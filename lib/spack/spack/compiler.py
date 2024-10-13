# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import itertools
import os
import platform
import re
import shutil
import sys
import tempfile
from typing import List, Optional, Sequence

import llnl.path
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import path_contains_subdirectory, paths_containing_libs

import spack.error
import spack.schema.environment
import spack.spec
import spack.util.executable
import spack.util.libc
import spack.util.module_cmd
import spack.version
from spack.util.environment import filter_system_paths

__all__ = ["Compiler"]

PATH_INSTANCE_VARS = ["cc", "cxx", "f77", "fc"]
FLAG_INSTANCE_VARS = ["cflags", "cppflags", "cxxflags", "fflags"]


@llnl.util.lang.memoized
def _get_compiler_version_output(compiler_path, version_arg, ignore_errors=()):
    """Invokes the compiler at a given path passing a single
    version argument and returns the output.

    Args:
        compiler_path (path): path of the compiler to be invoked
        version_arg (str): the argument used to extract version information
    """
    compiler = spack.util.executable.Executable(compiler_path)
    compiler_invocation_args = {
        "output": str,
        "error": str,
        "ignore_errors": ignore_errors,
        "timeout": 120,
        "fail_on_error": True,
    }
    if version_arg:
        output = compiler(version_arg, **compiler_invocation_args)
    else:
        output = compiler(**compiler_invocation_args)
    return output


def get_compiler_version_output(compiler_path, *args, **kwargs):
    """Wrapper for _get_compiler_version_output()."""
    # This ensures that we memoize compiler output by *absolute path*,
    # not just executable name. If we don't do this, and the path changes
    # (e.g., during testing), we can get incorrect results.
    if not os.path.isabs(compiler_path):
        compiler_path = spack.util.executable.which_string(compiler_path, required=True)

    return _get_compiler_version_output(compiler_path, *args, **kwargs)


def tokenize_flags(flags_values, propagate=False):
    """Given a compiler flag specification as a string, this returns a list
    where the entries are the flags. For compiler options which set values
    using the syntax "-flag value", this function groups flags and their
    values together. Any token not preceded by a "-" is considered the
    value of a prior flag."""
    tokens = flags_values.split()
    if not tokens:
        return []
    flag = tokens[0]
    flags_with_propagation = []
    for token in tokens[1:]:
        if not token.startswith("-"):
            flag += " " + token
        else:
            flags_with_propagation.append((flag, propagate))
            flag = token
    flags_with_propagation.append((flag, propagate))
    return flags_with_propagation


#: regex for parsing linker lines
_LINKER_LINE = re.compile(r"^( *|.*[/\\])" r"(link|ld|([^/\\]+-)?ld|collect2)" r"[^/\\]*( |$)")

#: components of linker lines to ignore
_LINKER_LINE_IGNORE = re.compile(r"(collect2 version|^[A-Za-z0-9_]+=|/ldfe )")

#: regex to match linker search paths
_LINK_DIR_ARG = re.compile(r"^-L(.:)?(?P<dir>[/\\].*)")

#: regex to match linker library path arguments
_LIBPATH_ARG = re.compile(r"^[-/](LIBPATH|libpath):(?P<dir>.*)")


def _parse_link_paths(string):
    """Parse implicit link paths from compiler debug output.

    This gives the compiler runtime library paths that we need to add to
    the RPATH of generated binaries and libraries.  It allows us to
    ensure, e.g., that codes load the right libstdc++ for their compiler.
    """
    lib_search_paths = False
    raw_link_dirs = []
    for line in string.splitlines():
        if lib_search_paths:
            if line.startswith("\t"):
                raw_link_dirs.append(line[1:])
                continue
            else:
                lib_search_paths = False
        elif line.startswith("Library search paths:"):
            lib_search_paths = True

        if not _LINKER_LINE.match(line):
            continue
        if _LINKER_LINE_IGNORE.match(line):
            continue
        tty.debug(f"implicit link dirs: link line: {line}")

        next_arg = False
        for arg in line.split():
            if arg in ("-L", "-Y"):
                next_arg = True
                continue

            if next_arg:
                raw_link_dirs.append(arg)
                next_arg = False
                continue

            link_dir_arg = _LINK_DIR_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group("dir")
                raw_link_dirs.append(link_dir)

            link_dir_arg = _LIBPATH_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group("dir")
                raw_link_dirs.append(link_dir)

    implicit_link_dirs = list()
    visited = set()
    for link_dir in raw_link_dirs:
        normalized_path = os.path.abspath(link_dir)
        if normalized_path not in visited:
            implicit_link_dirs.append(normalized_path)
            visited.add(normalized_path)

    tty.debug(f"implicit link dirs: result: {', '.join(implicit_link_dirs)}")
    return implicit_link_dirs


@llnl.path.system_path_filter
def _parse_non_system_link_dirs(string: str) -> List[str]:
    """Parses link paths out of compiler debug output.

    Args:
        string: compiler debug output as a string

    Returns:
        Implicit link paths parsed from the compiler output
    """
    link_dirs = _parse_link_paths(string)

    # Remove directories that do not exist. Some versions of the Cray compiler
    # report nonexistent directories
    link_dirs = [d for d in link_dirs if os.path.isdir(d)]

    # Return set of directories containing needed compiler libs, minus
    # system paths. Note that 'filter_system_paths' only checks for an
    # exact match, while 'in_system_subdirectory' checks if a path contains
    # a system directory as a subdirectory
    link_dirs = filter_system_paths(link_dirs)
    return list(p for p in link_dirs if not in_system_subdirectory(p))


def in_system_subdirectory(path):
    system_dirs = [
        "/lib/",
        "/lib64/",
        "/usr/lib/",
        "/usr/lib64/",
        "/usr/local/lib/",
        "/usr/local/lib64/",
    ]
    return any(path_contains_subdirectory(path, x) for x in system_dirs)


class Compiler:
    """This class encapsulates a Spack "compiler", which includes C,
    C++, and Fortran compilers.  Subclasses should implement
    support for specific compilers, their possible names, arguments,
    and how to identify the particular type of compiler."""

    # Optional prefix regexes for searching for this type of compiler.
    # Prefixes are sometimes used for toolchains
    prefixes: List[str] = []

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes = [r"-.*"]

    #: Compiler argument that produces version information
    version_argument = "-dumpversion"

    #: Return values to ignore when invoking the compiler to get its version
    ignore_version_errors: Sequence[int] = ()

    #: Regex used to extract version from compiler's output
    version_regex = "(.*)"

    # These libraries are anticipated to be required by all executables built
    # by any compiler
    _all_compiler_rpath_libraries = ["libc", "libc++", "libstdc++"]

    #: Platform matcher for Platform objects supported by compiler
    is_supported_on_platform = lambda x: True

    # Default flags used by a compiler to set an rpath
    @property
    def cc_rpath_arg(self):
        return "-Wl,-rpath,"

    @property
    def cxx_rpath_arg(self):
        return "-Wl,-rpath,"

    @property
    def f77_rpath_arg(self):
        return "-Wl,-rpath,"

    @property
    def fc_rpath_arg(self):
        return "-Wl,-rpath,"

    @property
    def linker_arg(self):
        """Flag that need to be used to pass an argument to the linker."""
        return "-Wl,"

    @property
    def disable_new_dtags(self):
        if platform.system() == "Darwin":
            return ""
        return "--disable-new-dtags"

    @property
    def enable_new_dtags(self):
        if platform.system() == "Darwin":
            return ""
        return "--enable-new-dtags"

    @property
    def debug_flags(self):
        return ["-g"]

    @property
    def opt_flags(self):
        return ["-O", "-O0", "-O1", "-O2", "-O3"]

    def __init__(
        self,
        cspec,
        operating_system,
        target,
        paths,
        modules=None,
        alias=None,
        environment=None,
        extra_rpaths=None,
        enable_implicit_rpaths=None,
        **kwargs,
    ):
        self.spec = cspec
        self.operating_system = str(operating_system)
        self.target = target
        self.modules = modules or []
        self.alias = alias
        self.environment = environment or {}
        self.extra_rpaths = extra_rpaths or []
        self.enable_implicit_rpaths = enable_implicit_rpaths

        self.cc = paths[0]
        self.cxx = paths[1]
        self.f77 = None
        self.fc = None
        if len(paths) > 2:
            self.f77 = paths[2]
            if len(paths) == 3:
                self.fc = self.f77
            else:
                self.fc = paths[3]

        # Unfortunately have to make sure these params are accepted
        # in the same order they are returned by sorted(flags)
        # in compilers/__init__.py
        self.flags = spack.spec.FlagMap(self.spec)
        for flag in self.flags.valid_compiler_flags():
            value = kwargs.get(flag, None)
            if value is not None:
                values_with_propagation = tokenize_flags(value, False)
                for value, propagation in values_with_propagation:
                    self.flags.add_flag(flag, value, propagation)

        # caching value for compiler reported version
        # used for version checks for API, e.g. C++11 flag
        self._real_version = None

    def __eq__(self, other):
        return (
            self.cc == other.cc
            and self.cxx == other.cxx
            and self.fc == other.fc
            and self.f77 == other.f77
            and self.spec == other.spec
            and self.operating_system == other.operating_system
            and self.target == other.target
            and self.flags == other.flags
            and self.modules == other.modules
            and self.environment == other.environment
            and self.extra_rpaths == other.extra_rpaths
            and self.enable_implicit_rpaths == other.enable_implicit_rpaths
        )

    def __hash__(self):
        return hash(
            (
                self.cc,
                self.cxx,
                self.fc,
                self.f77,
                self.spec,
                self.operating_system,
                self.target,
                str(self.flags),
                str(self.modules),
                str(self.environment),
                str(self.extra_rpaths),
                self.enable_implicit_rpaths,
            )
        )

    def verify_executables(self):
        """Raise an error if any of the compiler executables is not valid.

        This method confirms that for all of the compilers (cc, cxx, f77, fc)
        that have paths, those paths exist and are executable by the current
        user.
        Raises a CompilerAccessError if any of the non-null paths for the
        compiler are not accessible.
        """

        def accessible_exe(exe):
            # compilers may contain executable names (on Cray or user edited)
            if not os.path.isabs(exe):
                exe = spack.util.executable.which_string(exe)
                if not exe:
                    return False
            return os.path.isfile(exe) and os.access(exe, os.X_OK)

        # setup environment before verifying in case we have executable names
        # instead of absolute paths
        with self.compiler_environment():
            missing = [
                cmp
                for cmp in (self.cc, self.cxx, self.f77, self.fc)
                if cmp and not accessible_exe(cmp)
            ]
            if missing:
                raise CompilerAccessError(self, missing)

    @property
    def version(self):
        return self.spec.version

    @property
    def real_version(self):
        """Executable reported compiler version used for API-determinations

        E.g. C++11 flag checks.
        """
        if not self._real_version:
            try:
                real_version = spack.version.Version(self.get_real_version())
                if real_version == spack.version.Version("unknown"):
                    return self.version
                self._real_version = real_version
            except spack.util.executable.ProcessError:
                self._real_version = self.version
        return self._real_version

    def implicit_rpaths(self) -> List[str]:
        if self.enable_implicit_rpaths is False:
            return []

        output = self.compiler_verbose_output

        if not output:
            return []

        link_dirs = _parse_non_system_link_dirs(output)

        all_required_libs = list(self.required_libs) + Compiler._all_compiler_rpath_libraries
        return list(paths_containing_libs(link_dirs, all_required_libs))

    @property
    def default_dynamic_linker(self) -> Optional[str]:
        """Determine default dynamic linker from compiler link line"""
        output = self.compiler_verbose_output

        if not output:
            return None

        return spack.util.libc.parse_dynamic_linker(output)

    @property
    def default_libc(self) -> Optional["spack.spec.Spec"]:
        """Determine libc targeted by the compiler from link line"""
        dynamic_linker = self.default_dynamic_linker

        if not dynamic_linker:
            return None

        return spack.util.libc.libc_from_dynamic_linker(dynamic_linker)

    @property
    def required_libs(self):
        """For executables created with this compiler, the compiler libraries
        that would be generally required to run it.
        """
        # By default every compiler returns the empty list
        return []

    @property
    def compiler_verbose_output(self) -> Optional[str]:
        """Verbose output from compiling a dummy C source file. Output is cached."""
        if not hasattr(self, "_compile_c_source_output"):
            self._compile_c_source_output = self._compile_dummy_c_source()
        return self._compile_c_source_output

    def _compile_dummy_c_source(self) -> Optional[str]:
        cc = self.cc if self.cc else self.cxx
        if not cc or not self.verbose_flag:
            return None

        try:
            tmpdir = tempfile.mkdtemp(prefix="spack-implicit-link-info")
            fout = os.path.join(tmpdir, "output")
            fin = os.path.join(tmpdir, "main.c")

            with open(fin, "w") as csource:
                csource.write(
                    "int main(int argc, char* argv[]) { (void)argc; (void)argv; return 0; }\n"
                )
            cc_exe = spack.util.executable.Executable(cc)
            for flag_type in ["cflags" if cc == self.cc else "cxxflags", "cppflags", "ldflags"]:
                cc_exe.add_default_arg(*self.flags.get(flag_type, []))

            with self.compiler_environment():
                return cc_exe(self.verbose_flag, fin, "-o", fout, output=str, error=str)
        except spack.util.executable.ProcessError as pe:
            tty.debug("ProcessError: Command exited with non-zero status: " + pe.long_message)
            return None
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @property
    def verbose_flag(self) -> Optional[str]:
        """
        This property should be overridden in the compiler subclass if a
        verbose flag is available.

        If it is not overridden, it is assumed to not be supported.
        """

    # This property should be overridden in the compiler subclass if
    # OpenMP is supported by that compiler
    @property
    def openmp_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "OpenMP", "openmp_flag")

    # This property should be overridden in the compiler subclass if
    # C++98 is not the default standard for that compiler
    @property
    def cxx98_flag(self):
        return ""

    # This property should be overridden in the compiler subclass if
    # C++11 is supported by that compiler
    @property
    def cxx11_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "the C++11 standard", "cxx11_flag")

    # This property should be overridden in the compiler subclass if
    # C++14 is supported by that compiler
    @property
    def cxx14_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "the C++14 standard", "cxx14_flag")

    # This property should be overridden in the compiler subclass if
    # C++17 is supported by that compiler
    @property
    def cxx17_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "the C++17 standard", "cxx17_flag")

    # This property should be overridden in the compiler subclass if
    # C99 is supported by that compiler
    @property
    def c99_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "the C99 standard", "c99_flag")

    # This property should be overridden in the compiler subclass if
    # C11 is supported by that compiler
    @property
    def c11_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self, "the C11 standard", "c11_flag")

    @property
    def cc_pic_flag(self):
        """Returns the flag used by the C compiler to produce
        Position Independent Code (PIC)."""
        return "-fPIC"

    @property
    def cxx_pic_flag(self):
        """Returns the flag used by the C++ compiler to produce
        Position Independent Code (PIC)."""
        return "-fPIC"

    @property
    def f77_pic_flag(self):
        """Returns the flag used by the F77 compiler to produce
        Position Independent Code (PIC)."""
        return "-fPIC"

    @property
    def fc_pic_flag(self):
        """Returns the flag used by the FC compiler to produce
        Position Independent Code (PIC)."""
        return "-fPIC"

    # Note: This is not a class method. The class methods are used to detect
    # compilers on PATH based systems, and do not set up the run environment of
    # the compiler. This method can be called on `module` based systems as well
    def get_real_version(self):
        """Query the compiler for its version.

        This is the "real" compiler version, regardless of what is in the
        compilers.yaml file, which the user can change to name their compiler.

        Use the runtime environment of the compiler (modules and environment
        modifications) to enable the compiler to run properly on any platform.
        """
        cc = spack.util.executable.Executable(self.cc)
        with self.compiler_environment():
            output = cc(
                self.version_argument,
                output=str,
                error=str,
                ignore_errors=tuple(self.ignore_version_errors),
            )
            return self.extract_version_from_output(output)

    @property
    def prefix(self):
        """Query the compiler for its install prefix. This is the install
        path as reported by the compiler. Note that paths for cc, cxx, etc
        are not enough to find the install prefix of the compiler, since
        the can be symlinks, wrappers, or filenames instead of absolute paths."""
        raise NotImplementedError("prefix is not implemented for this compiler")

    #
    # Compiler classes have methods for querying the version of
    # specific compiler executables.  This is used when discovering compilers.
    #
    # Compiler *instances* are just data objects, and can only be
    # constructed from an actual set of executables.
    #
    @classmethod
    def default_version(cls, cc):
        """Override just this to override all compiler version functions."""
        output = get_compiler_version_output(
            cc, cls.version_argument, tuple(cls.ignore_version_errors)
        )
        return cls.extract_version_from_output(output)

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        """Extracts the version from compiler's output."""
        match = re.search(cls.version_regex, output)
        return match.group(1) if match else "unknown"

    @classmethod
    def cc_version(cls, cc):
        return cls.default_version(cc)

    @classmethod
    def search_regexps(cls, language):
        # Compile all the regular expressions used for files beforehand.
        # This searches for any combination of <prefix><name><suffix>
        # defined for the compiler
        compiler_names = getattr(cls, "{0}_names".format(language))
        prefixes = [""] + cls.prefixes
        suffixes = [""]
        if sys.platform == "win32":
            ext = r"\.(?:exe|bat)"
            cls_suf = [suf + ext for suf in cls.suffixes]
            ext_suf = [ext]
            suffixes = suffixes + cls.suffixes + cls_suf + ext_suf
        else:
            suffixes = suffixes + cls.suffixes
        regexp_fmt = r"^({0}){1}({2})$"
        return [
            re.compile(regexp_fmt.format(prefix, re.escape(name), suffix))
            for prefix, name, suffix in itertools.product(prefixes, compiler_names, suffixes)
        ]

    def setup_custom_environment(self, pkg, env):
        """Set any environment variables necessary to use the compiler."""
        pass

    def __repr__(self):
        """Return a string representation of the compiler toolchain."""
        return self.__str__()

    def __str__(self):
        """Return a string representation of the compiler toolchain."""
        return "%s(%s)" % (
            self.name,
            "\n     ".join(
                (
                    str(s)
                    for s in (
                        self.cc,
                        self.cxx,
                        self.f77,
                        self.fc,
                        self.modules,
                        str(self.operating_system),
                    )
                )
            ),
        )

    @contextlib.contextmanager
    def compiler_environment(self):
        # Avoid modifying os.environ if possible.
        if not self.modules and not self.environment:
            yield
            return

        # store environment to replace later
        backup_env = os.environ.copy()

        try:
            # load modules and set env variables
            for module in self.modules:
                spack.util.module_cmd.load_module(module)

            # apply other compiler environment changes
            spack.schema.environment.parse(self.environment).apply_modifications()

            yield
        finally:
            # Restore environment regardless of whether inner code succeeded
            os.environ.clear()
            os.environ.update(backup_env)

    def to_dict(self):
        flags_dict = {fname: " ".join(fvals) for fname, fvals in self.flags.items()}
        flags_dict.update(
            {attr: getattr(self, attr, None) for attr in FLAG_INSTANCE_VARS if hasattr(self, attr)}
        )
        result = {
            "spec": str(self.spec),
            "paths": {attr: getattr(self, attr, None) for attr in PATH_INSTANCE_VARS},
            "flags": flags_dict,
            "operating_system": str(self.operating_system),
            "target": str(self.target),
            "modules": self.modules or [],
            "environment": self.environment or {},
            "extra_rpaths": self.extra_rpaths or [],
        }

        if self.enable_implicit_rpaths is not None:
            result["implicit_rpaths"] = self.enable_implicit_rpaths

        if self.alias:
            result["alias"] = self.alias

        return result


class CompilerAccessError(spack.error.SpackError):
    def __init__(self, compiler, paths):
        msg = "Compiler '%s' has executables that are missing" % compiler.spec
        msg += " or are not executable: %s" % paths
        super().__init__(msg)


class InvalidCompilerError(spack.error.SpackError):
    def __init__(self):
        super().__init__("Compiler has no executables.")


class UnsupportedCompilerFlag(spack.error.SpackError):
    def __init__(self, compiler, feature, flag_name, ver_string=None):
        super().__init__(
            "{0} ({1}) does not support {2} (as compiler.{3}).".format(
                compiler.name, ver_string if ver_string else compiler.version, feature, flag_name
            ),
            "If you think it should, please edit the compiler.{0} subclass to".format(
                compiler.name
            )
            + " implement the {0} property and submit a pull request or issue.".format(flag_name),
        )
