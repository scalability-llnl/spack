# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpt(BundlePackage):
    """HPE MPI is HPE's implementation of
    the Message Passing Interface (MPI) standard.

    Note: HPE MPI is proprietry software. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://buy.hpe.com/us/en/software/high-performance-computing-software/hpe-message-passing-interface-mpi/p/1010144155"

    # https://support.hpe.com/hpesc/public/swd/detail?swItemId=MTX-4b90e0f8e3224ce3bc3644d6ad
    version("1.4")

    provides("mpi")
    provides("mpi@:3.1", when="@3:")
    provides("mpi@:1.3", when="@1:")

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ["libmpi"]

        if "cxx" in query_parameters:
            libraries = ["libmpicxx"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=True, recursive=True)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # use the Spack compiler wrappers under MPI
        dependent_module = dependent_spec.package.module
        env.set("MPICC_CC", dependent_module.spack_cc)
        env.set("MPICXX_CXX", dependent_module.spack_cxx)
        env.set("MPIF90_F90", dependent_module.spack_fc)

    def setup_run_environment(self, env):
        # Because MPI is both runtime and compiler, we have to setup the mpi
        # compilers as part of the run environment.
        env.set("MPICC", self.prefix.bin.mpicc)
        env.set("MPICXX", self.prefix.bin.mpicxx)
        env.set("MPIF77", self.prefix.bin.mpif77)
        env.set("MPIF90", self.prefix.bin.mpif90)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = self.prefix.bin.mpicc
        self.spec.mpicxx = self.prefix.bin.mpicxx
        self.spec.mpifc = self.prefix.bin.mpif90
        self.spec.mpif77 = self.prefix.bin.mpif77
