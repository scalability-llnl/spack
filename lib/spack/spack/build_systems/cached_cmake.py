# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from llnl.util.filesystem import install, mkdirp
import llnl.util.tty as tty

from spack.build_systems.cmake import CMakePackage
from spack.package import run_after


def cmake_cache_path(name, value, comment=""):
    """Generate a string for a cmake cache variable"""
    return 'set({0} "{1}" CACHE PATH "{2}")\n'.format(name, value, comment)


def cmake_cache_string(name, value, comment=""):
    """Generate a string for a cmake cache variable"""
    return 'set({0} "{1}" CACHE STRING "{2}")\n'.format(name, value, comment)


def cmake_cache_option(name, boolean_value, comment=""):
    """Generate a string for a cmake configuration option"""

    value = "ON" if boolean_value else "OFF"
    return 'set({0} {1} CACHE BOOL "{2}")\n'.format(name, value, comment)


class CachedCMakePackage(CMakePackage):
    """Specialized class for packages built using CMake initial cache.

    This feature of CMake allows packages to increase reproducibility,
    especially between Spack- and manual builds. It also allows packages to
    sidestep certain parsing bugs in extremely long ``cmake`` commands, and to
    avoid system limits on the length of the command line."""

    phases = ['initconfig', 'cmake', 'build', 'install']

    @property
    def cache_name(self):
        return "{0}-{1}-{2}@{3}.cmake".format(
            self.name,
            self.spec.architecture,
            self.spec.compiler.name,
            self.spec.compiler.version,
        )

    @property
    def cache_path(self):
        return os.path.join(self.stage.source_path, self.cache_name)

    def flag_handler(self, name, flags):
        if name in ('cflags', 'cxxflags', 'cppflags', 'fflags'):
            return (None, None, None)  # handled in the cmake cache
        return (flags, None, None)

    def initconfig_compiler_entries(self):
        # This will tell cmake to use the Spack compiler wrappers when run
        # through Spack, but use the underlying compiler when run outside of
        # Spack
        spec = self.spec

        # Fortran compiler is optional
        if "FC" in os.environ:
            spack_fc_entry = cmake_cache_path(
                "CMAKE_Fortran_COMPILER", os.environ['FC'])
            system_fc_entry = cmake_cache_path(
                "CMAKE_Fortran_COMPILER", self.compiler.fc)
        else:
            spack_fc_entry = "# No Fortran compiler defined in spec"
            system_fc_entry = "# No Fortran compiler defined in spec"

        entries = [
            "#------------------{0}".format("-" * 60),
            "# Compilers",
            "#------------------{0}".format("-" * 60),
            "# Compiler Spec: {0}".format(spec.compiler),
            "#------------------{0}".format("-" * 60),
            'if(DEFINED ENV{SPACK_CC})\n',
            '  ' + cmake_cache_path(
                "CMAKE_C_COMPILER", os.environ['CC']),
            '  ' + cmake_cache_path(
                "CMAKE_CXX_COMPILER", os.environ['CXX']),
            '  ' + spack_fc_entry,
            'else()\n',
            '  ' + cmake_cache_path(
                "CMAKE_C_COMPILER", self.compiler.cc),
            '  ' + cmake_cache_path(
                "CMAKE_CXX_COMPILER", self.compiler.cxx),
            '  ' + system_fc_entry,
            'endif()\n'
        ]

        # use global spack compiler flags
        cppflags = ' '.join(spec.compiler_flags['cppflags'])
        if cppflags:
            # avoid always ending up with ' ' with no flags defined
            cppflags += ' '
        cflags = cppflags + ' '.join(spec.compiler_flags['cflags'])
        if cflags:
            entries.append(cmake_cache_string("CMAKE_C_FLAGS", cflags))
        cxxflags = cppflags + ' '.join(spec.compiler_flags['cxxflags'])
        if cxxflags:
            entries.append(cmake_cache_string("CMAKE_CXX_FLAGS", cxxflags))
        fflags = ' '.join(spec.compiler_flags['fflags'])
        if fflags:
            entries.append(cmake_cache_string("CMAKE_Fortran_FLAGS", fflags))

        # Override XL compiler family
        familymsg = ("Override to proper compiler family for XL")
        if "xlf" in (self.compiler.fc or ''):  # noqa: F821
            entries.append(cmake_cache_string(
                "CMAKE_Fortran_COMPILER_ID", "XL",
                familymsg))
        if "xlc" in self.compiler.cc:  # noqa: F821
            entries.append(cmake_cache_string(
                "CMAKE_C_COMPILER_ID", "XL",
                familymsg))
        if "xlC" in self.compiler.cxx:  # noqa: F821
            entries.append(cmake_cache_string(
                "CMAKE_CXX_COMPILER_ID", "XL",
                familymsg))

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec

        if not spec.satisfies('^mpi'):
            return []

        entries = [
            "#------------------{0}".format("-" * 60),
            "# MPI",
            "#------------------{0}\n".format("-" * 60),
        ]

        entries.append(cmake_cache_path("MPI_C_COMPILER",
                                        spec['mpi'].mpicc))
        entries.append(cmake_cache_path("MPI_CXX_COMPILER",
                                        spec['mpi'].mpicxx))
        entries.append(cmake_cache_path("MPI_Fortran_COMPILER",
                                        spec['mpi'].mpifc))

        # Check for slurm
        using_slurm = False
        slurm_checks = ['+slurm',
                        'schedulers=slurm',
                        'process_managers=slurm']
        if any(spec['mpi'].satisfies(variant) for variant in slurm_checks):
            using_slurm = True

        # Determine MPIEXEC
        if using_slurm:
            if spec['mpi'].external:
                # Heuristic until we have dependents on externals
                mpiexec = '/usr/bin/srun'
            else:
                mpiexec = os.path.join(spec['slurm'].prefix.bin, 'srun')
        else:
            mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpirun')
            if not os.path.exists(mpiexec):
                mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpiexec')

        if not os.path.exists(mpiexec):
            msg = "Unable to determine MPIEXEC, %s tests may fail" % self.name
            entries.append("# {0}\n".format(msg))
            tty.warn(msg)
        else:
            # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
            # vs the older versions which expect MPIEXEC
            if self.spec["cmake"].satisfies('@3.10:'):
                entries.append(cmake_cache_path("MPIEXEC_EXECUTABLE",
                                                mpiexec))
            else:
                entries.append(cmake_cache_path("MPIEXEC", mpiexec))

        # Determine MPIEXEC_NUMPROC_FLAG
        if using_slurm:
            entries.append(cmake_cache_string("MPIEXEC_NUMPROC_FLAG", "-n"))
        else:
            entries.append(cmake_cache_string("MPIEXEC_NUMPROC_FLAG", "-np"))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec

        entries = [
            "#------------------{0}".format("-" * 60),
            "# Hardware",
            "#------------------{0}\n".format("-" * 60),
        ]

        if spec.satisfies('^cuda'):
            entries.append("#------------------{0}".format("-" * 30))
            entries.append("# Cuda")
            entries.append("#------------------{0}\n".format("-" * 30))

            cudatoolkitdir = spec['cuda'].prefix
            entries.append(cmake_cache_path("CUDA_TOOLKIT_ROOT_DIR",
                                            cudatoolkitdir))
            cudacompiler = "${CUDA_TOOLKIT_ROOT_DIR}/bin/nvcc"
            entries.append(cmake_cache_path("CMAKE_CUDA_COMPILER",
                                            cudacompiler))

            if spec.satisfies('^mpi'):
                entries.append(cmake_cache_path("CMAKE_CUDA_HOST_COMPILER",
                                                "${MPI_CXX_COMPILER}"))
            else:
                entries.append(cmake_cache_path("CMAKE_CUDA_HOST_COMPILER",
                                                "${CMAKE_CXX_COMPILER}"))

        return entries

    def std_initconfig_entries(self):
        return [
            "#------------------{0}".format("-" * 60),
            "# !!!! This is a generated file, edit at own risk !!!!",
            "#------------------{0}".format("-" * 60),
            "# CMake executable path: {0}".format(
                self.spec['cmake'].command.path),
            "#------------------{0}\n".format("-" * 60),
        ]

    def initconfig(self, spec, prefix):
        cache_entries = (self.std_initconfig_entries() +
                         self.initconfig_compiler_entries() +
                         self.initconfig_mpi_entries() +
                         self.initconfig_hardware_entries() +
                         self.initconfig_package_entries())

        with open(self.cache_name, 'w') as f:
            for entry in cache_entries:
                f.write('%s\n' % entry)
            f.write('\n')

    @property
    def std_cmake_args(self):
        args = super(CachedCMakePackage, self).std_cmake_args
        args.extend(['-C', self.cache_path])
        return args

    @run_after('install')
    def install_cmake_cache(self):
        mkdirp(self.spec.prefix.share.cmake)
        install(self.cache_path, self.spec.prefix.share.cmake)
