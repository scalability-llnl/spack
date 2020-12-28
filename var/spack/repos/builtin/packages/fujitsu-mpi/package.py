# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class FujitsuMpi(Package):
    """Fujitsu MPI implementation only for Fujitsu compiler."""

    homepage = "https://www.fujitsu.com/us/"

    conflicts('%arm')
    conflicts('%cce')
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%gcc')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    provides('mpi@3.1:')

    def install(self, spec, prefix):
        raise InstallError(
            'Fujitsu MPI is not installable; it is vendor supplied')

    @property
    def headers(self):
        hdrs = find_headers('mpi', self.prefix.include, recursive=True)
        hdrs.directories = os.path.dirname(hdrs[0])
        return hdrs or None

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpi_cxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = self.prefix.bin.mpifcc
        self.spec.mpicxx = self.prefix.bin.mpiFCC
        self.spec.mpif77 = self.prefix.bin.mpifrt
        self.spec.mpifc = self.prefix.bin.mpifrt

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def setup_run_environment(self, env):
        # Because MPI are both compilers and runtimes, we set up the compilers
        # as part of run environment
        env.set('MPICC', self.prefix.bin.mpifcc)
        env.set('MPICXX', self.prefix.bin.mpiFCC)
        env.set('MPIF77', self.prefix.bin.mpifrt)
        env.set('MPIF90', self.prefix.bin.mpifrt)
