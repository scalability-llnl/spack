# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import re
import subprocess

import archspec.cpu

import spack.build_systems.compiler
import spack.platforms
import spack.version
from spack.package import *


class Msvc(Package, CompilerPackage):
    """
    Microsoft Visual C++ is a compiler for the C, C++, C++/CLI and C++/CX programming languages.
    """

    homepage = "https://visualstudio.microsoft.com/vs/features/cplusplus/"

    def install(self, spec, prefix):
        raise InstallError(
            "MSVC compilers are not installable with Spack, but can be "
            "detected on a system where they are externally installed"
        )

    compiler_languages = ["c", "cxx"]
    c_names = ["cl"]
    cxx_names = ["cl"]
    compiler_version_argument = ""
    compiler_version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"

    # Named wrapper links within build_env_path
    # Due to the challenges of supporting compiler wrappers
    # in Windows, we leave these blank, and dynamically compute
    # based on proper versions of MSVC from there
    # pending acceptance of #28117 for full support using
    # compiler wrappers
    link_paths = {"c": "", "cxx": "", "fortran": ""}

    provides("c", "cxx")
    requires("platform=windows", msg="MSVC is only supported on Windows")

    @classmethod
    def determine_version(cls, exe):
        # MSVC compiler does not have a proper version argument
        # Errors out and prints version info with no args
        match = re.search(
            cls.compiler_version_regex,
            spack.build_systems.compiler.compiler_output(
                exe, version_argument=None, ignore_errors=1
            ),
        )
        if match:
            return match.group(1)

    @classmethod
    def determine_variants(cls, exes, version_str):
        # MSVC uses same executable for both languages
        spec, extras = super().determine_variants(exes, version_str)
        extras["compilers"]["c"] = extras["compilers"]["cxx"]
        return spec, extras

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.init_msvc()
        # Set the build environment variables for spack. Just using
        # subprocess.call() doesn't work since that operates in its own
        # environment which is destroyed (along with the adjusted variables)
        # once the process terminates. So go the long way around: examine
        # output, sort into dictionary, use that to make the build
        # environment.

        # vcvars can target specific sdk versions, force it to pick up concretized sdk
        # version, if needed by spec
        if dependent_spec.name != "win-sdk" and "win-sdk" in dependent_spec:
            self.vcvars_call.sdk_ver = dependent_spec["win-sdk"].version.string

        out = self.msvc_compiler_environment()
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

        env.set("CC", self.cc)
        env.set("CXX", self.cxx)

    def init_msvc(self):
        # To use the MSVC compilers, VCVARS must be invoked
        # VCVARS is located at a fixed location, referencable
        # idiomatically by the following relative path from the
        # compiler.
        # Spack first finds the compilers via VSWHERE
        # and stores their path, but their respective VCVARS
        # file must be invoked before useage.
        env_cmds = []
        compiler_root = os.path.join(os.path.dirname(self.cc), "../../../../../..")
        vcvars_script_path = os.path.join(compiler_root, "Auxiliary", "Build", "vcvars64.bat")
        # get current platform architecture and format for vcvars argument
        arch = spack.platforms.real_host().default.lower()
        arch = arch.replace("-", "_")
        if str(archspec.cpu.host().family) == "x86_64":
            arch = "amd64"

        msvc_version = spack.version.Version(
            re.search(Msvc.compiler_version_regex, self.cc).group(1)
        )
        self.vcvars_call = VCVarsInvocation(vcvars_script_path, arch, msvc_version)
        env_cmds.append(self.vcvars_call)
        self.msvc_compiler_environment = CmdCall(*env_cmds)

    def _standard_flag(self, *, language: str, standard: str) -> str:
        flags = {
            "cxx": {
                "11": "/std:c++11",
                "14": "/std:c++14",
                "17": "/std:c++17",
                "20": "/std:c++20",
            },
            "c": {"11": "/std:c11", "17": "/std:c17"},
        }
        return flags[language][standard]

    @property
    def short_msvc_version(self):
        """This is the shorthand VCToolset version of form
        MSVC<short-ver>
        """
        return "MSVC" + self.vc_toolset_ver

    @property
    def vc_toolset_ver(self):
        """
        The toolset version is the version of the combined set of cl and link
        This typically relates directly to VS version i.e. VS 2022 is v143
        VS 19 is v142, etc.
        This value is defined by the first three digits of the major + minor
        version of the VS toolset (143 for 14.3x.bbbbb). Traditionally the
        minor version has remained a static two digit number for a VS release
        series, however, as of VS22, this is no longer true, both
        14.4x.bbbbb and 14.3x.bbbbb are considered valid VS22 VC toolset
        versions due to a change in toolset minor version sentiment.

        This is *NOT* the full version, for that see
        Msvc.msvc_version or MSVC.platform_toolset_ver for the
        raw platform toolset version

        """
        ver = self.msvc_version[:2].joined.string[:3]
        return ver

    @property
    def msvc_version(self):
        """This is the VCToolset version *NOT* the actual version of the cl compiler"""
        return spack.version.Version(re.search(Msvc.compiler_version_regex, self.cc).group(1))

    @property
    def vs_root(self):
        # The MSVC install root is located at a fix level above the compiler
        # and is referenceable idiomatically via the pattern below
        # this should be consistent accross versions
        return os.path.abspath(os.path.join(self.cc, "../../../../../../../.."))

    @property
    def platform_toolset_ver(self):
        """
        This is the platform toolset version of current MSVC compiler
        i.e. 142. The platform toolset is the targeted MSVC library/compiler
        versions by compilation (this is different from the VC Toolset)


        This is different from the VC toolset version as established
        by `short_msvc_version`, but typically are represented by the same
        three digit value
        """
        # Typically VS toolset version and platform toolset versions match
        # VS22 introduces the first divergence of VS toolset version
        # (144 for "recent" releases) and platform toolset version (143)
        # so it needs additional handling until MS releases v144
        # (assuming v144 is also for VS22)
        # or adds better support for detection
        # TODO: (johnwparent) Update this logic for the next platform toolset
        # or VC toolset version update
        toolset_ver = self.vc_toolset_ver
        vs22_toolset = spack.version.Version(toolset_ver) > Version("142")
        return toolset_ver if not vs22_toolset else "143"


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


FC_PATH = {}


def get_valid_fortran_pth():
    """Assign maximum available fortran compiler version"""
    # TODO (johnwparent): validate compatibility w/ try compiler
    # functionality when added
    sort_fn = lambda fc_ver: spack.version.Version(fc_ver)
    sort_fc_ver = sorted(list(FC_PATH.keys()), key=sort_fn)
    return FC_PATH[sort_fc_ver[-1]] if sort_fc_ver else None
