# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import inspect
import os
import platform
import re
from typing import List  # novm

import spack.build_environment
from llnl.util.filesystem import working_dir
from spack.util.environment import filter_system_paths
from spack.directives import depends_on, variant, conflicts
from spack.package_base import PackageBase, InstallError, run_after

# Regex to extract the primary generator from the CMake generator
# string.
_primary_generator_extractor = re.compile(r'(?:.* - )?(.*)')


def _extract_primary_generator(generator):
    """Use the compiled regex _primary_generator_extractor to extract the
    primary generator from the generator string which may contain an
    optional secondary generator.
    """
    primary_generator = _primary_generator_extractor.match(generator).group(1)
    return primary_generator


class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake

    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/

    This class provides three phases that can be overridden:

        1. :py:meth:`~.CMakePackage.cmake`
        2. :py:meth:`~.CMakePackage.build`
        3. :py:meth:`~.CMakePackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.CMakePackage.cmake_args`.
    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.CMakePackage.root_cmakelists_dir` | Location of the    |
        |                                               | root CMakeLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.CMakePackage.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+


    The generator used by CMake can be specified by providing the
    generator attribute. Per
    https://cmake.org/cmake/help/git-master/manual/cmake-generators.7.html,
    the format is: [<secondary-generator> - ]<primary_generator>. The
    full list of primary and secondary generators supported by CMake may
    be found in the documentation for the version of CMake used;
    however, at this time Spack supports only the primary generators
    "Unix Makefiles" and "Ninja." Spack's CMake support is agnostic with
    respect to primary generators. Spack will generate a runtime error
    if the generator string does not follow the prescribed format, or if
    the primary generator is not supported.
    """
    #: Phases of a CMake package
    phases = ['cmake', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'CMakePackage'

    build_targets = []  # type: List[str]
    install_targets = ['install']

    build_time_test_callbacks = ['check']

    #: The build system generator to use.
    #:
    #: See ``cmake --help`` for a list of valid generators.
    #: Currently, "Unix Makefiles" and "Ninja" are the only generators
    #: that Spack supports. Defaults to "Unix Makefiles".
    #:
    #: See https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html
    #: for more information.
    generator = 'Unix Makefiles'

    # https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html
    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    # https://cmake.org/cmake/help/latest/variable/CMAKE_INTERPROCEDURAL_OPTIMIZATION.html
    variant('ipo', default=False,
            description='CMake interprocedural optimization')
    # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
    conflicts('+ipo', when='^cmake@:3.8',
              msg='+ipo is not supported by CMake < 3.9')

    depends_on('cmake', type='build')

    @property
    def archive_files(self):
        """Files to archive for packages based on CMake"""
        return [os.path.join(self.build_directory, 'CMakeCache.txt')]

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return self.stage.source_path

    @property
    def std_cmake_args(self):
        """Standard cmake arguments provided as a property for
        convenience of package writers

        :return: standard cmake arguments
        """
        # standard CMake arguments
        std_cmake_args = CMakePackage._std_args(self)
        std_cmake_args += getattr(self, 'cmake_flag_args', [])
        return std_cmake_args

    @staticmethod
    def _std_args(pkg):
        """Computes the standard cmake arguments for a generic package"""
        try:
            generator = pkg.generator
        except AttributeError:
            generator = 'Unix Makefiles'

        # Make sure a valid generator was chosen
        valid_primary_generators = ['Unix Makefiles', 'Ninja']
        primary_generator = _extract_primary_generator(generator)
        if primary_generator not in valid_primary_generators:
            msg  = "Invalid CMake generator: '{0}'\n".format(generator)
            msg += "CMakePackage currently supports the following "
            msg += "primary generators: '{0}'".\
                   format("', '".join(valid_primary_generators))
            raise InstallError(msg)

        try:
            build_type = pkg.spec.variants['build_type'].value
        except KeyError:
            build_type = 'RelWithDebInfo'

        try:
            ipo = pkg.spec.variants['ipo'].value
        except KeyError:
            ipo = False

        define = CMakePackage.define
        args = [
            '-G', generator,
            define('CMAKE_INSTALL_PREFIX', pkg.prefix),
            define('CMAKE_BUILD_TYPE', build_type),
        ]

        # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
        if pkg.spec.satisfies('^cmake@3.9:'):
            args.append(define('CMAKE_INTERPROCEDURAL_OPTIMIZATION', ipo))

        if primary_generator == 'Unix Makefiles':
            args.append(define('CMAKE_VERBOSE_MAKEFILE', True))

        if platform.mac_ver()[0]:
            args.extend([
                define('CMAKE_FIND_FRAMEWORK', "LAST"),
                define('CMAKE_FIND_APPBUNDLE', "LAST"),
            ])

        # Set up CMake rpath
        args.extend([
            define('CMAKE_INSTALL_RPATH_USE_LINK_PATH', False),
            define('CMAKE_INSTALL_RPATH',
                   spack.build_environment.get_rpaths(pkg)),
        ])
        # CMake's find_package() looks in CMAKE_PREFIX_PATH first, help CMake
        # to find immediate link dependencies in right places:
        deps = [d.prefix for d in
                pkg.spec.dependencies(deptype=('build', 'link'))]
        deps = filter_system_paths(deps)
        args.append(define('CMAKE_PREFIX_PATH', deps))
        return args

    @staticmethod
    def define(cmake_var, value):
        """Return a CMake command line argument that defines a variable.

        The resulting argument will convert boolean values to OFF/ON
        and lists/tuples to CMake semicolon-separated string lists. All other
        values will be interpreted as strings.

        Examples:

            .. code-block:: python

                [define('BUILD_SHARED_LIBS', True),
                 define('CMAKE_CXX_STANDARD', 14),
                 define('swr', ['avx', 'avx2'])]

            will generate the following configuration options:

            .. code-block:: console

                ["-DBUILD_SHARED_LIBS:BOOL=ON",
                 "-DCMAKE_CXX_STANDARD:STRING=14",
                 "-DSWR:STRING=avx;avx2]

        """
        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        if isinstance(value, bool):
            kind = 'BOOL'
            value = "ON" if value else "OFF"
        else:
            kind = 'STRING'
            if isinstance(value, (list, tuple)):
                value = ";".join(str(v) for v in value)
            else:
                value = str(value)

        return "".join(["-D", cmake_var, ":", kind, "=", value])

    def define_from_variant(self, cmake_var, variant=None):
        """Return a CMake command line argument from the given variant's value.

        The optional ``variant`` argument defaults to the lower-case transform
        of ``cmake_var``.

        This utility function is similar to
        :py:meth:`~.AutotoolsPackage.with_or_without`.

        Examples:

            Given a package with:

            .. code-block:: python

                variant('cxxstd', default='11', values=('11', '14'),
                        multi=False, description='')
                variant('shared', default=True, description='')
                variant('swr', values=any_combination_of('avx', 'avx2'),
                        description='')

            calling this function like:

            .. code-block:: python

                [define_from_variant('BUILD_SHARED_LIBS', 'shared'),
                 define_from_variant('CMAKE_CXX_STANDARD', 'cxxstd'),
                 define_from_variant('SWR')]

            will generate the following configuration options:

            .. code-block:: console

                ["-DBUILD_SHARED_LIBS:BOOL=ON",
                 "-DCMAKE_CXX_STANDARD:STRING=14",
                 "-DSWR:STRING=avx;avx2]

            for ``<spec-name> cxxstd=14 +shared swr=avx,avx2``
        """

        if variant is None:
            variant = cmake_var.lower()

        if variant not in self.variants:
            raise KeyError(
                '"{0}" is not a variant of "{1}"'.format(variant, self.name))

        value = self.spec.variants[variant].value
        if isinstance(value, (tuple, list)):
            # Sort multi-valued variants for reproducibility
            value = sorted(value)

        return self.define(cmake_var, value)

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass the specified
        compiler flags to cmake. Note CMAKE does not have a cppflags option,
        so cppflags will be added to cflags, cxxflags, and fflags to mimic the
        behavior in other tools."""
        # Has to be dynamic attribute due to caching
        setattr(self, 'cmake_flag_args', [])

        flag_string = '-DCMAKE_{0}_FLAGS={1}'
        langs = {'C': 'c', 'CXX': 'cxx', 'Fortran': 'f'}

        # Handle language compiler flags
        for lang, pre in langs.items():
            flag = pre + 'flags'
            # cmake has no explicit cppflags support -> add it to all langs
            lang_flags = ' '.join(flags.get(flag, []) + flags.get('cppflags',
                                                                  []))
            if lang_flags:
                self.cmake_flag_args.append(flag_string.format(lang,
                                                               lang_flags))

        # Cmake has different linker arguments for different build types.
        # We specify for each of them.
        if flags['ldflags']:
            ldflags = ' '.join(flags['ldflags'])
            ld_string = '-DCMAKE_{0}_LINKER_FLAGS={1}'
            # cmake has separate linker arguments for types of builds.
            for type in ['EXE', 'MODULE', 'SHARED', 'STATIC']:
                self.cmake_flag_args.append(ld_string.format(type, ldflags))

        # CMake has libs options separated by language. Apply ours to each.
        if flags['ldlibs']:
            libs_flags = ' '.join(flags['ldlibs'])
            libs_string = '-DCMAKE_{0}_STANDARD_LIBRARIES={1}'
            for lang in langs:
                self.cmake_flag_args.append(libs_string.format(lang,
                                                               libs_flags))

    @property
    def build_dirname(self):
        """Returns the directory name to use when building the package

        :return: name of the subdirectory for building the package
        """
        return 'spack-build-%s' % self.spec.dag_hash(7)

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return os.path.join(self.stage.path, self.build_dirname)

    def cmake_args(self):
        """Produces a list containing all the arguments that must be passed to
        cmake, except:

            * CMAKE_INSTALL_PREFIX
            * CMAKE_BUILD_TYPE

        which will be set automatically.

        :return: list of arguments for cmake
        """
        return []

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory"""
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*options)

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.build_targets)
            elif self.generator == 'Ninja':
                self.build_targets.append("-v")
                inspect.getmodule(self).ninja(*self.build_targets)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.install_targets)
            elif self.generator == 'Ninja':
                inspect.getmodule(self).ninja(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                self._if_make_target_execute('test',
                                             jobs_env='CTEST_PARALLEL_LEVEL')
                self._if_make_target_execute('check')
            elif self.generator == 'Ninja':
                self._if_ninja_target_execute('test',
                                              jobs_env='CTEST_PARALLEL_LEVEL')
                self._if_ninja_target_execute('check')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
