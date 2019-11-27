# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import itertools
import shutil
import tempfile

import llnl.util.lang
from llnl.util.filesystem import (
    path_contains_subdirectory, paths_containing_libs)
import llnl.util.tty as tty

import spack.error
import spack.spec
import spack.architecture
import spack.util.executable
import spack.compilers
from spack.util.environment import filter_system_paths

__all__ = ['Compiler']


def _verify_executables(*paths):
    for path in paths:
        if not os.path.isfile(path) and os.access(path, os.X_OK):
            raise CompilerAccessError(path)


@llnl.util.lang.memoized
def get_compiler_version_output(compiler_path, version_arg):
    """Invokes the compiler at a given path passing a single
    version argument and returns the output.

    Args:
        compiler_path (path): path of the compiler to be invoked
        version_arg (str): the argument used to extract version information
    """
    compiler = spack.util.executable.Executable(compiler_path)
    output = compiler(version_arg, output=str, error=str)
    return output


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
    cc_names = []

    # Subclasses use possible names of C++ compiler
    cxx_names = []

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = []

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = []

    # Optional prefix regexes for searching for this type of compiler.
    # Prefixes are sometimes used for toolchains, e.g. 'powerpc-bgq-linux-'
    prefixes = []

    # Optional suffix regexes for searching for this type of compiler.
    # Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    # version suffix for gcc.
    suffixes = [r'-.*']

    #: Compiler argument that produces version information
    version_argument = '-dumpversion'

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

    # Cray PrgEnv name that can be used to load this compiler
    cray_prgenv_name = None
    # Name of module used to switch versions of this compiler
    cray_module_name = None

    def __init__(self, cspec, operating_system, target,
                 paths, modules=[], alias=None, environment=None,
                 extra_rpaths=None, enable_implicit_rpaths=None,
                 **kwargs):
        self.spec = cspec
        self.operating_system = str(operating_system)
        self.target = target
        self.modules = modules
        self.alias = alias
        self.extra_rpaths = extra_rpaths
        self.enable_implicit_rpaths = enable_implicit_rpaths

        def check(exe):
            if exe is None:
                return None
            _verify_executables(exe)
            return exe

        self.cc  = check(paths[0])
        self.cxx = check(paths[1])
        if len(paths) > 2:
            self.f77 = check(paths[2])
            if len(paths) == 3:
                self.fc = self.f77
            else:
                self.fc  = check(paths[3])

        self.environment = environment
        self.extra_rpaths = extra_rpaths or []

        # Unfortunately have to make sure these params are accepted
        # in the same order they are returned by sorted(flags)
        # in compilers/__init__.py
        self.flags = {}
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            value = kwargs.get(flag, None)
            if value is not None:
                self.flags[flag] = tokenize_flags(value)

    @property
    def version(self):
        return self.spec.version

    def implicit_rpaths(self):
        if self.enable_implicit_rpaths is False:
            return []

        exe_paths = [
            x for x in [self.cc, self.cxx, self.fc, self.f77] if x]
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

    @classmethod
    def _get_compiler_link_paths(cls, paths):
        first_compiler = next((c for c in paths if c), None)
        if not first_compiler:
            return []

        try:
            tmpdir = tempfile.mkdtemp(prefix='spack-implicit-link-info')
            fout = os.path.join(tmpdir, 'output')
            fin = os.path.join(tmpdir, 'main.c')

            with open(fin, 'w+') as csource:
                csource.write(
                    'int main(int argc, char* argv[]) { '
                    '(void)argc; (void)argv; return 0; }\n')
            compiler_exe = spack.util.executable.Executable(first_compiler)
            output = str(compiler_exe(cls.verbose_flag(), fin, '-o', fout,
                                      output=str, error=str))  # str for py2

            return _parse_non_system_link_dirs(output)
        except spack.util.executable.ProcessError as pe:
            tty.debug('ProcessError: Command exited with non-zero status: ' +
                      pe.long_message)
            return []
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @classmethod
    def verbose_flag(cls):
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
        output = get_compiler_version_output(cc, cls.version_argument)
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


class CompilerAccessError(spack.error.SpackError):

    def __init__(self, path):
        super(CompilerAccessError, self).__init__(
            "'%s' is not a valid compiler." % path)


class InvalidCompilerError(spack.error.SpackError):

    def __init__(self):
        super(InvalidCompilerError, self).__init__(
            "Compiler has no executables.")


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
