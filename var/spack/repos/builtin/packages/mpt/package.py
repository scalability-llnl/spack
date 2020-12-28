# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpt(Package):
    """HPE MPI is HPE's implementation of
    the Message Passing Interface (MPI) standard.

    Note: HPE MPI is proprietry software. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://buy.hpe.com/us/en/software/high-performance-computing-software/hpe-message-passing-interface-mpi/p/1010144155"

    provides('mpi')
    provides('mpi@:3.1', when='@3:')
    provides('mpi@:1.3', when='@1:')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpif08',
        relative_root='bin'
    )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

        # use the Spack compiler wrappers under MPI
        env.set('MPICC_CC', spack_cc)
        env.set('MPICXX_CXX', spack_cxx)
        env.set('MPIF90_F90', spack_fc)

    def setup_run_environment(self, env):
        # Because MPI is both runtime and compiler, we have to setup the mpi
        # compilers as part of the run environment.
        env.set('MPICC',  self.prefix.bin.mpicc)
        env.set('MPICXX', self.prefix.bin.mpicxx)
        env.set('MPIF77', self.prefix.bin.mpif77)
        env.set('MPIF90', self.prefix.bin.mpif90)

    def setup_dependent_package(self, module, dependent_spec):
        if 'platform=cray' in self.spec:
            self.spec.mpicc = spack_cc
            self.spec.mpicxx = spack_cxx
            self.spec.mpifc = spack_fc
            self.spec.mpif77 = spack_f77
        else:
            self.spec.mpicc = self.prefix.bin.mpicc
            self.spec.mpicxx = self.prefix.bin.mpicxx
            self.spec.mpifc = self.prefix.bin.mpif90
            self.spec.mpif77 = self.prefix.bin.mpif77

    @property
    def fetcher(self):
        msg = """This package is a placeholder for HPE MPI, a
        system-provided, proprietary MPI implementation.

        Add to your packages.yaml (changing the /opt/ path to match
        where HPE MPI is actually installed):

        packages:
          mpt:
            buildable: False
            externals:
            - spec: mpt@2.20
              prefix: /opt
        """
        raise InstallError(msg)
