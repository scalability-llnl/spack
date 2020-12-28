# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class CrayMpich(Package):
    """Cray's MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False    # Skip attempts to fetch source that is not available

    maintainers = ['haampie']

    version('8.1.0')
    version('8.0.16')
    version('8.0.14')
    version('8.0.11')
    version('8.0.9')
    version('7.7.16')
    version('7.7.15')
    version('7.7.14')
    version('7.7.13')

    provides('mpi@3')

    def setup_run_environment(self, env):
        env.set('MPICC', spack_cc)
        env.set('MPICXX', spack_cxx)
        env.set('MPIF77', spack_fc)
        env.set('MPIF90', spack_fc)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        spec = self.spec
        spec.mpicc = spack_cc
        spec.mpicxx = spack_cxx
        spec.mpifc = spack_fc
        spec.mpif77 = spack_f77

        spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpicxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))
