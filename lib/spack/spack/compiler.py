# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import os
import platform
import re
import itertools
import shutil
import tempfile
from typing import Sequence, List  # novm

import llnl.util.lang
from llnl.util.filesystem import (
    path_contains_subdirectory, paths_containing_libs)
import llnl.util.tty as tty

import spack.error
import spack.spec
import spack.version
import spack.architecture
import spack.util.executable
import spack.util.module_cmd
import spack.compilers
from spack.util.environment import filter_system_paths

__all__ = ['Compiler']


@llnl.util.lang.memoized
def _get_compiler_version_output(compiler_path, version_arg, ignore_errors=()):
    """Invokes the compiler at a given path passing a single
    version argument and returns the output.

    Args:
        compiler_path (path): path of the compiler to be invoked
        version_arg (str): the argument used to extract version information
    """
    compiler = spack.util.executable.Executable(compiler_path)
    output = compiler(
        version_arg, output=str, error=str, ignore_errors=ignore_errors)
    return output


def get_compiler_version_output(compiler_path, *args, **kwargs):
    """Wrapper for _get_compiler_version_output()."""
    # This ensures that we memoize compiler output by *absolute path*,
    # not just executable name. If we don't do this, and the path changes
    # (e.g., during testing), we can get incorrect results.
    if not os.path.isabs(compiler_path):
        compiler_path = spack.util.executable.which_string(
            compiler_path, required=True)

    return _get_compiler_version_output(compiler_path, *args, **kwargs)


def tokenize_flags(flags_str):
    """Given a compiler flag specification as a string, this returns a list
       where the entries are the flags. For compiler options which set values
       using the syntax "-flag value", this function groups flags and their
       values together. Any token not preceded by a "-" is considered the
       value of a prior flag."""
    tokens = flags_str.split()
    if not tokens:
        return []
    flag = tokens[0]
    flags = []
    for token in tokens[1:]:
        if not token.startswith('-'):
            flag += ' ' + token
        else:
            flags.append(flag)
            flag = token
    flags.append(flag)
    return flags


#: regex for parsing linker lines
_LINKER_LINE = re.compile(
    r'^( *|.*[/\\])'
    r'(link|ld|([^/\\]+-)?ld|collect2)'
    r'[^/\\]*( |$)')

#: components of linker lines to ignore
_LINKER_LINE_IGNORE = re.compile(r'(collect2 version|^[A-Za-z0-9_]+=|/ldfe )')

#: regex to match linker search paths
_LINK_DIR_ARG = re.compile(r'^-L(.:)?(?P<dir>[/\\].*)')

#: regex to match linker library path arguments
_LIBPATH_ARG = re.compile(r'^[-/](LIBPATH|libpath):(?P<dir>.*)')


def _parse_link_paths(string):
    """Parse implicit link paths from compiler debug output.

    This gives the compiler runtime library paths that we need to add to
    the RPATH of generated binaries and libraries.  It allows us to
    ensure, e.g., that codes load the right libstdc++ for their compiler.
    """
    lib_search_paths = False
    raw_link_dirs = []
    tty.debug('parsing implicit link info')
    for line in string.splitlines():
        if lib_search_paths:
            if line.startswith('\t'):
                raw_link_dirs.append(line[1:])
                continue
            else:
                lib_search_paths = False
        elif line.startswith('Library search paths:'):
            lib_search_paths = True

        if not _LINKER_LINE.match(line):
            continue
        if _LINKER_LINE_IGNORE.match(line):
            continue
        tty.debug('linker line: %s' % line)

        next_arg = False
        for arg in line.split():
            if arg in ('-L', '-Y'):
                next_arg = True
                continue

            if next_arg:
                raw_link_dirs.append(arg)
                next_arg = False
                continue

            link_dir_arg = _LINK_DIR_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group('dir')
                tty.debug('linkdir: %s' % link_dir)
                raw_link_dirs.append(link_dir)

            link_dir_arg = _LIBPATH_ARG.match(arg)
            if link_dir_arg:
                link_dir = link_dir_arg.group('dir')
                tty.debug('libpath: %s', link_dir)
                raw_link_dirs.append(link_dir)
    tty.debug('found raw link dirs: %s' % ', '.join(raw_link_dirs))

    implicit_link_dirs = list()
    visited = set()
    for link_dir in raw_link_dirs:
        normalized_path = os.path.abspath(link_dir)
        if normalized_path not in visited:
            implicit_link_dirs.append(normalized_path)
            visited.add(normalized_path)

    tty.debug('found link dirs: %s' % ', '.join(implicit_link_dirs))
    return implicit_link_dirs


def _parse_non_system_link_dirs(string):
    """Parses link paths out of compiler debug output.

    Args:
        string (str): compiler debug output as a string

    Returns:
        (list of str): implicit link paths parsed from the compiler output
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
    system_dirs = ['/lib/', '/lib64/', '/usr/lib/', '/usr/lib64/',
                   '/usr/local/lib/', '/usr/local/lib64/']
    return any(path_contains_subdirectory(path, x) for x in system_dirs)


class Compiler(object):
    """This class encapsulates a Spack "compiler", which includes C,
       C++, and Fortran compilers.  Subclasses should implement
       support for specific compilers, their possible names, arguments,
       and how to identify the particular type of compiler."""

    # Subclasses use possible names of C compiler
    cc_names = []  # type: List[str]

    # Subclasses use possible names of C++ compiler
    cxx_names = []  # type: List[str]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []  # type: List[str]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []  # type: List[str]

    # Optional prefix regexes for searching for this type of compiler.
    # Prefixes are sometimes used for toolchains
    prefixes = []  # type: List[str]

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes = [r'-.*']

    #: Compiler argument that produces version information
    version_argument = '-dumpversion'

    #: Return values to ignore when invoking the compiler to get its version
    ignore_version_errors = ()  # type: Sequence[int]

    #: Regex used to extract version from compiler's output
    version_regex = '(.*)'

    # These libraries are anticipated to be required by all executables built
    # by any compiler
    _all_compiler_rpath_libraries = ['libc', 'libc++', 'libstdc++']

    # Default flags used by a compiler to set an rpath
    @property
    def cc_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def cxx_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def f77_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def fc_rpath_arg(self):
        return '-Wl,-rpath,'

    @property
    def linker_arg(self):
        """Flag that need to be used to pass an argument to the linker."""
        return '-Wl,'

    @property
    def disable_new_dtags(self):
        if platform.system() == 'Darwin':
            return ''
        return '--disable-new-dtags'

    @property
    def enable_new_dtags(self):
        if platform.system() == 'Darwin':
            return ''
        return '--enable-new-dtags'

    @property
    def debug_flags(self):
        return ['-g']

    @property
    def opt_flags(self):
        return ['-O', '-O0', '-O1', '-O2', '-O3']

    # Cray PrgEnv name that can be used to load this compiler
    PrgEnv = None  # type: str
    # Name of module used to switch versions of this compiler
    PrgEnv_compiler = None  # type: str

    def __init__(self, cspec, operating_system, target,
                 paths, modules=None, alias=None, environment=None,
                 extra_rpaths=None, enable_implicit_rpaths=None,
                 **kwargs):
        self.spec = cspec
        self.operating_system = str(operating_system)
        self.target = target
        self.modules = modules or []
        self.alias = alias
        self.environment = environment or {}
        self.extra_rpaths = extra_rpaths or []
        self.enable_implicit_rpaths = enable_implicit_rpaths

        self.cc  = paths[0]
        self.cxx = paths[1]
        self.f77 = None
        self.fc = None
        if len(paths) > 2:
            self.f77 = paths[2]
            if len(paths) == 3:
                self.fc = self.f77
            else:
                self.fc  = paths[3]

        # Unfortunately have to make sure these params are accepted
        # in the same order they are returned by sorted(flags)
        # in compilers/__init__.py
        self.flags = {}
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            value = kwargs.get(flag, None)
            if value is not None:
                self.flags[flag] = tokenize_flags(value)

        # caching value for compiler reported version
        # used for version checks for API, e.g. C++11 flag
        self._real_version = None

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
        with self._compiler_environment():
            missing = [cmp for cmp in (self.cc, self.cxx, self.f77, self.fc)
                       if cmp and not accessible_exe(cmp)]
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
                self._real_version = spack.version.Version(
                    self.get_real_version())
            except spack.util.executable.ProcessError:
                self._real_version = self.version
        return self._real_version

    def implicit_rpaths(self):
        if self.enable_implicit_rpaths is False:
            return []

        # Put CXX first since it has the most linking issues
        # And because it has flags that affect linking
        exe_paths = [
            x for x in [self.cxx, self.cc, self.fc, self.f77] if x]
        link_dirs = self._get_compiler_link_paths(exe_paths)

        all_required_libs = (
            list(self.required_libs) + Compiler._all_compiler_rpath_libraries)
        return list(paths_containing_libs(link_dirs, all_required_libs))

    @property
    def required_libs(self):
        """For executables created with this compiler, the compiler libraries
        that would be generally required to run it.
        """
        # By default every compiler returns the empty list
        return []

    def _get_compiler_link_paths(self, paths):
        first_compiler = next((c for c in paths if c), None)
        if not first_compiler:
            return []
        if not self.verbose_flag:
            # In this case there is no mechanism to learn what link directories
            # are used by the compiler
            return []

        # What flag types apply to first_compiler, in what order
        flags = ['cppflags', 'ldflags']
        if first_compiler == self.cc:
            flags = ['cflags'] + flags
        elif first_compiler == self.cxx:
            flags = ['cxxflags'] + flags
        else:
            flags.append('fflags')

        try:
            tmpdir = tempfile.mkdtemp(prefix='spack-implicit-link-info')
            fout = os.path.join(tmpdir, 'output')
            fin = os.path.join(tmpdir, 'main.c')

            with open(fin, 'w+') as csource:
                csource.write(
                    'int main(int argc, char* argv[]) { '
                    '(void)argc; (void)argv; return 0; }\n')
            compiler_exe = spack.util.executable.Executable(first_compiler)
            for flag_type in flags:
                for flag in self.flags.get(flag_type, []):
                    compiler_exe.add_default_arg(flag)

            output = ''
            with self._compiler_environment():
                output = str(compiler_exe(
                    self.verbose_flag, fin, '-o', fout,
                    output=str, error=str))  # str for py2
            return _parse_non_system_link_dirs(output)
        except spack.util.executable.ProcessError as pe:
            tty.debug('ProcessError: Command exited with non-zero status: ' +
                      pe.long_message)
            return []
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @property
    def verbose_flag(self):
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
        raise UnsupportedCompilerFlag(self,
                                      "the C++11 standard",
                                      "cxx11_flag")

    # This property should be overridden in the compiler subclass if
    # C++14 is supported by that compiler
    @property
    def cxx14_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C++14 standard",
                                      "cxx14_flag")

    # This property should be overridden in the compiler subclass if
    # C++17 is supported by that compiler
    @property
    def cxx17_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C++17 standard",
                                      "cxx17_flag")

    # This property should be overridden in the compiler subclass if
    # C99 is supported by that compiler
    @property
    def c99_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C99 standard",
                                      "c99_flag")

    # This property should be overridden in the compiler subclass if
    # C11 is supported by that compiler
    @property
    def c11_flag(self):
        # If it is not overridden, assume it is not supported and warn the user
        raise UnsupportedCompilerFlag(self,
                                      "the C11 standard",
                                      "c11_flag")

    @property
    def cc_pic_flag(self):
        """Returns the flag used by the C compiler to produce
        Position Independent Code (PIC)."""
        return '-fPIC'

    @property
    def cxx_pic_flag(self):
        """Returns the flag used by the C++ compiler to produce
        Position Independent Code (PIC)."""
        return '-fPIC'

    @property
    def f77_pic_flag(self):
        """Returns the flag used by the F77 compiler to produce
        Position Independent Code (PIC)."""
        return '-fPIC'

    @property
    def fc_pic_flag(self):
        """Returns the flag used by the FC compiler to produce
        Position Independent Code (PIC)."""
        return '-fPIC'

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
        with self._compiler_environment():
            output = cc(self.version_argument,
                        output=str, error=str,
                        ignore_errors=tuple(self.ignore_version_errors))
            return self.extract_version_from_output(output)

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
            cc, cls.version_argument, tuple(cls.ignore_version_errors))
        return cls.extract_version_from_output(output)

    @classmethod
    @llnl.util.lang.memoized
    def extract_version_from_output(cls, output):
        """Extracts the version from compiler's output."""
        match = re.search(cls.version_regex, output)
        return match.group(1) if match else 'unknown'

    @classmethod
    def cc_version(cls, cc):
        return cls.default_version(cc)

    @classmethod
    def cxx_version(cls, cxx):
        return cls.default_version(cxx)

    @classmethod
    def f77_version(cls, f77):
        return cls.default_version(f77)

    @classmethod
    def fc_version(cls, fc):
        return cls.default_version(fc)

    @classmethod
    def search_regexps(cls, language):
        # Compile all the regular expressions used for files beforehand.
        # This searches for any combination of <prefix><name><suffix>
        # defined for the compiler
        compiler_names = getattr(cls, '{0}_names'.format(language))
        prefixes = [''] + cls.prefixes
        suffixes = [''] + cls.suffixes
        regexp_fmt = r'^({0}){1}({2})$'
        return [
            re.compile(regexp_fmt.format(prefix, re.escape(name), suffix))
            for prefix, name, suffix in
            itertools.product(prefixes, compiler_names, suffixes)
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
            self.name, '\n     '.join((str(s) for s in (
                self.cc, self.cxx, self.f77, self.fc, self.modules,
                str(self.operating_system)))))

    @contextlib.contextmanager
    def _compiler_environment(self):
        # store environment to replace later
        backup_env = os.environ.copy()

        try:
            if (self.modules
                and os.environ.get("CRAY_CPU_TARGET") == 'mic-knl'):
                # On cray, mic-knl module cannot be loaded without cce module
                # See: https://github.com/spack/spack/issues/3153
                spack.util.module_cmd.load_module('cce')

            # load modules and set env variables
            for module in self.modules:
                spack.util.module_cmd.load_module(module)

            loaded_modules = os.environ.get("LOADEDMODULES", "").split(":")

            for module in self.modules:
                if module not in loaded_modules:
                    raise InvalidCompilerModuleError(self, module)

            # apply other compiler environment changes
            env = spack.util.environment.EnvironmentModifications()
            env.extend(spack.schema.environment.parse(self.environment))
            env.apply_modifications()

            yield
        except BaseException:
            raise
        finally:
            # Restore environment regardless of whether inner code succeeded
            os.environ.clear()
            os.environ.update(backup_env)


class CompilerAccessError(spack.error.SpackError):
    def __init__(self, compiler, paths):
        msg = "Compiler '%s' has executables that are missing" % compiler.spec
        msg += " or are not executable: %s" % paths
        super(CompilerAccessError, self).__init__(msg)


class InvalidCompilerError(spack.error.SpackError):

    def __init__(self):
        super(InvalidCompilerError, self).__init__(
            "Compiler has no executables.")


class InvalidCompilerModuleError(spack.error.SpackError):
    def __init__(self, compiler, module):
        msg = ("Module specified for compiler '{0}' could not be loaded: {1}"
               .format(compiler.spec, module))
        super(InvalidCompilerModuleError, self).__init__(msg)


class UnsupportedCompilerFlag(spack.error.SpackError):

    def __init__(self, compiler, feature, flag_name, ver_string=None):
        super(UnsupportedCompilerFlag, self).__init__(
            "{0} ({1}) does not support {2} (as compiler.{3})."
            .format(compiler.name,
                    ver_string if ver_string else compiler.version,
                    feature,
                    flag_name),
            "If you think it should, please edit the compiler.{0} subclass to"
            .format(compiler.name) +
            " implement the {0} property and submit a pull request or issue."
            .format(flag_name)
        )
