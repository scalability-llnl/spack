# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Sequence, Type

import archspec.cpu

import spack.compiler
import spack.operating_systems.windows_os
import spack.platforms
import spack.util.executable
from spack.compiler import Compiler
from spack.error import SpackError
from spack.version import Version, VersionRange

FC_PATH: Dict[str, str] = dict()


class CmdCall:
    """Compose a call to `cmd` for an ordered series of cmd commands/scripts"""

    def __init__(self, *cmds):
        if not cmds:
            raise RuntimeError(
                """Attempting to run commands from CMD without specifying commands.
                Please add commands to be run."""
            )
        self._cmds = cmds

    def __call__(self):
        out = subprocess.check_output(self.cmd_line, stderr=subprocess.STDOUT)  # novermin
        return out.decode("utf-16le", errors="replace")  # novermin

    @property
    def cmd_line(self):
        base_call = "cmd /u /c "
        commands = " && ".join([x.command_str() for x in self._cmds])
        # If multiple commands are being invoked by a single subshell
        # they must be encapsulated by a double quote. Always double
        # quote to be sure of proper handling
        # cmd will properly resolve nested double quotes as needed
        #
        # `set`` writes out the active env to the subshell stdout,
        # and in this context we are always trying to obtain env
        # state so it should always be appended
        return base_call + f'"{commands} && set"'


class VarsInvocation:
    def __init__(self, script):
        self._script = script

    def command_str(self):
        return f'"{self._script}"'

    @property
    def script(self):
        return self._script


class VCVarsInvocation(VarsInvocation):
    def __init__(self, script, arch, msvc_version):
        super(VCVarsInvocation, self).__init__(script)
        self._arch = arch
        self._msvc_version = msvc_version

    @property
    def sdk_ver(self):
        """Accessor for Windows SDK version property

        Note: This property may not be set by
        the calling context and as such this property will
        return an empty string

        This property will ONLY be set if the SDK package
        is a dependency somewhere in the Spack DAG of the package
        for which we are constructing an MSVC compiler env.
        Otherwise this property should be unset to allow the VCVARS
        script to use its internal heuristics to determine appropriate
        SDK version
        """
        if getattr(self, "_sdk_ver", None):
            return self._sdk_ver + ".0"
        return ""

    @sdk_ver.setter
    def sdk_ver(self, val):
        self._sdk_ver = val

    @property
    def arch(self):
        return self._arch

    @property
    def vcvars_ver(self):
        return f"-vcvars_ver={self._msvc_version}"

    def command_str(self):
        script = super(VCVarsInvocation, self).command_str()
        return f"{script} {self.arch} {self.sdk_ver} {self.vcvars_ver}"


def get_valid_fortran_pth():
    """Assign maximum available fortran compiler version"""
    # TODO (johnwparent): validate compatibility w/ try compiler
    # functionality when added
    sort_fn = lambda fc_ver: Version(fc_ver)
    sort_fc_ver = sorted(list(FC_PATH.keys()), key=sort_fn)
    return FC_PATH[sort_fc_ver[-1]] if sort_fc_ver else None


class Msvc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names: List[str] = ["cl"]

    # Subclasses use possible names of C++ compiler
    cxx_names: List[str] = ["cl"]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names: List[str] = ["ifx"]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names: List[str] = ["ifx"]

    # Named wrapper links within build_env_path
    # Due to the challenges of supporting compiler wrappers
    # in Windows, we leave these blank, and dynamically compute
    # based on proper versions of MSVC from there
    # pending acceptance of #28117 for full support using
    # compiler wrappers
    link_paths = {"cc": "", "cxx": "", "f77": "", "fc": ""}

    #: Compiler argument that produces version information
    version_argument = ""

    # For getting ifx's version, call it with version_argument
    # and ignore the error code
    ignore_version_errors = [1]

    #: Regex used to extract version from compiler's output
    version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"
    # The MSVC compiler class overrides this to prevent instances
    # of erroneous matching on executable names that cannot be msvc
    # compilers
    suffixes = []

    #: List denoting supported platforms by compiler
    supported_platforms: Sequence[Type[spack.platforms.Platform]] = [
        spack.platforms.Windows,
        spack.platforms.Test,
    ]

    #: compiler argument used for compiling and not linking
    compile_only_arg = "/c"

    def __init__(self, *args, **kwargs):
        # This positional argument "paths" is later parsed and process by the base class
        # via the call to `super` later in this method
        paths = args[3]
        latest_fc = get_valid_fortran_pth()
        new_pth = [pth if pth else latest_fc for pth in paths[2:]]
        paths[2:] = new_pth
        # Initialize, deferring to base class but then adding the vcvarsallfile
        # file based on compiler executable path.
        super().__init__(*args, **kwargs)
        # To use the MSVC compilers, VCVARS must be invoked
        # VCVARS is located at a fixed location, referencable
        # idiomatically by the following relative path from the
        # compiler.
        # Spack first finds the compilers via VSWHERE
        # and stores their path, but their respective VCVARS
        # file must be invoked before useage.
        env_cmds = []
        # get current platform architecture and format for vcvars argument
        arch = spack.platforms.real_host().default.lower()
        arch = arch.replace("-", "_")
        if str(archspec.cpu.host().family) == "x86_64":
            arch = "amd64"

        self.vcvars_call = VCVarsInvocation(self.vcvarsall_for_cl(self.cc), arch, self.msvc_version)
        env_cmds = [self.vcvars_call]
        # Below is a check for a valid fortran path
        # paths has c, cxx, fc, and f77 paths in that order
        # paths[2] refers to the fc path and is a generic check
        # for a fortran compiler
        if paths[2]:
            # If this found, it sets all the vars
            oneapi_root_setvars = self.setvars_for_fc(self.fc)
            oneapi_version_setvars = self.setvars_for_fc_version(self.fc)
            # order matters here, the specific version env must be invoked first,
            # otherwise it will be ignored if the root setvars sets up the oneapi
            # env first
            env_cmds.extend(
                [VarsInvocation(oneapi_version_setvars), VarsInvocation(oneapi_root_setvars)]
            )
        self.msvc_compiler_environment = CmdCall(*env_cmds)

    @property
    def msvc_version(self):
        """This is the VCToolset version *NOT* the actual version of the cl compiler
        For CL version, query `Msvc.cl_version`"""
        return self._msvc_version(self.cc)

    @property
    def short_msvc_version(self):
        """
        This is the shorthand VCToolset version of form
        MSVC<short-ver> *NOT* the full version, for that see
        Msvc.msvc_version or MSVC.platform_toolset_ver for the
        raw platform toolset version
        """
        ver = self.platform_toolset_ver
        return "MSVC" + ver

    @property
    def platform_toolset_ver(self):
        """
        This is the platform toolset version of current MSVC compiler
        i.e. 142.
        This is different from the VC toolset version as established
        by `short_msvc_version`
        """
        return self.msvc_version[:2].joined.string[:3]

    @property
    def cl_version(self):
        """Cl toolset version"""
        return self._compiler_version(self.cc)

    @property
    def ifx_version(self):
        """Ifx compiler version associated with this version of MSVC"""
        return self._compiler_version(self.fc)

    @property
    def vs_root(self):
        # The MSVC install root is located at a fix level above the compiler
        # and is referenceable idiomatically via the pattern below
        # this should be consistent accross versions
        return os.path.abspath(os.path.join(self.cc, "../../../../../../../.."))

    def setup_custom_environment(self, pkg, env):
        """Set environment variables for MSVC using the
        Microsoft-provided script."""
        # Set the build environment variables for spack. Just using
        # subprocess.call() doesn't work since that operates in its own
        # environment which is destroyed (along with the adjusted variables)
        # once the process terminates. So go the long way around: examine
        # output, sort into dictionary, use that to make the build
        # environment.

        # vcvars can target specific sdk versions, force it to pick up concretized sdk
        # version, if needed by spec
        if pkg.name != "win-sdk" and "win-sdk" in pkg.spec:
            self.vcvars_call.sdk_ver = pkg.spec["win-sdk"].version.string

        out = self.msvc_compiler_environment()
        self.parse_vars_output(out, env)

        # certain versions of ifx (2021.3.0:2023.1.0) do not play well with env:TMP
        # that has a "." character in the path
        # Work around by pointing tmp to the stage for the duration of the build
        if self.fc and Version(self.fc_version(self.fc)).satisfies(
            VersionRange("2021.3.0", "2023.1.0")
        ):
            new_tmp = tempfile.mkdtemp(dir=pkg.stage.path)
            env.set("TMP", new_tmp)

        env.set("CC", self.cc)
        env.set("CXX", self.cxx)
        env.set("FC", self.fc)
        env.set("F77", self.f77)

    @classmethod
    def fc_version(cls, fc):
        if not sys.platform == "win32":
            return "unknown"
        fc_ver = cls.default_version(fc)
        FC_PATH[fc_ver] = fc
        try:
            sps = spack.operating_systems.windows_os.WindowsOs().compiler_search_paths
        except AttributeError:
            raise SpackError(
                "Windows compiler search paths not established, "
                "please report this behavior to github.com/spack/spack"
            )
        clp = spack.util.executable.which_string("cl", path=sps)
        return cls.default_version(clp) if clp else fc_ver

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)

    @classmethod
    def parse_vars_output(cls, out, env):
        int_env = dict(
            (key, value)
            for key, _, value in (line.partition("=") for line in out.splitlines())
            if key and value
        )
        for env_var in int_env:
            if os.pathsep not in int_env[env_var]:
                env.set(env_var, int_env[env_var])
            else:
                env.set_path(env_var, int_env[env_var].split(os.pathsep))

    @classmethod
    def _msvc_version(cls, cl):
        return Version(re.search(cls.version_regex, cl).group(1))

    @classmethod
    def _compiler_version(self, compiler):
        """Returns version object for given compiler"""
        # ignore_errors below is true here due to ifx's
        # non zero return code if it is not provided
        # and input file
        return Version(
            re.search(
                Msvc.version_regex,
                spack.compiler.get_compiler_version_output(
                    compiler, version_arg=None, ignore_errors=True
                ),
            ).group(1)
        )

    @classmethod
    def vcvarsall_for_cl(cls, cl):
        compiler_root = (
            pathlib.Path(cl) / ".." / ".." / ".." / ".." / ".." / ".." / ".."
        ).resolve()
        return str(compiler_root / "Auxiliary" / "Build" / "vcvarsall.bat")

    @classmethod
    def oneapi_root(cls, fc):
        """From within a prefix known to be a oneAPI path
        determine the oneAPI root path from arbitrary point
        under root

        Args:
            fc: path prefixed within oneAPI root
        """
        if not fc:
            return ""
        root_pth = [x for x in pathlib.Path(fc).parents if x.name == "oneAPI"]
        root_pth = root_pth[0] if root_pth else ""
        return root_pth

    @classmethod
    def setvars_for_fc(cls, fc):
        setvars_root = cls.oneapi_root(fc)
        if not setvars_root:
            raise RuntimeError(f"Non-oneAPI Fortran compiler {fc} assigned to MSVC")
        return str(setvars_root / "setvars.bat")

    @classmethod
    def setvars_for_fc_version(cls, fc):
        setvars_root = cls.oneapi_root(fc)
        # some oneAPI exes return a version more precise than their
        # install paths specify, so we determine path from
        # the install path rather than the fc executable itself
        numver = r"\d+\.\d+(?:\.\d+)?"
        pattern = f"((?:{numver})|(?:latest))"
        version_from_path = re.search(pattern, fc).group(1)
        return str(setvars_root / "compiler" / version_from_path / "env" / "vars.bat")

    def _cmp_test_env(self):
        env = spack.util.environment.EnvironmentModifications()
        out = self.msvc_compiler_environment()
        self.parse_vars_output(out, env)
        return env

    @contextlib.contextmanager
    def compiler_environment(self):
        # Avoid modifying os.environ if possible.
        # store environment to replace later
        backup_env = os.environ.copy()

        try:
            env = self._cmp_test_env()
            env.apply_modifications()

            yield
        finally:
            # Restore environment regardless of whether inner code succeeded
            os.environ.clear()
            os.environ.update(backup_env)