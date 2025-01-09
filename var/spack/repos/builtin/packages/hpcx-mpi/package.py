# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HpcxMpi(Package):
    """The HPC-X MPI implementation from NVIDIA/Mellanox based on OpenMPI.
    This package is for external specs only."""

    homepage = "https://developer.nvidia.com/networking/hpc-x"
    maintainers("mwkrentel")

    has_code = False

    provides("mpi")

    requires("platform=linux")

    def install(self, spec, prefix):
        raise InstallError("HPC-X MPI is not buildable, it is for external specs only.")

    def setup_dependent_package(self, module, dependent_spec):
        # This works for AOCC (AMD), Intel and GNU.
        self.spec.mpicc = os.path.join(self.prefix.bin, "mpicc")
        self.spec.mpicxx = os.path.join(self.prefix.bin, "mpicxx")
        self.spec.mpif77 = os.path.join(self.prefix.bin, "mpif77")
        self.spec.mpifc = os.path.join(self.prefix.bin, "mpif90")

    def make_base_environment(self, prefix, env):
        env.set("MPICC", os.path.join(prefix.bin, "mpicc"))
        env.set("MPICXX", os.path.join(prefix.bin, "mpicxx"))
        env.set("MPIF77", os.path.join(prefix.bin, "mpif77"))
        env.set("MPIF90", os.path.join(prefix.bin, "mpif90"))
        env.prepend_path("LD_LIBRARY_PATH", prefix.lib)
        env.set("OPAL_PREFIX", prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.make_base_environment(self.prefix, env)

    def setup_run_environment(self, env):
        self.make_base_environment(self.prefix, env)
