# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.mpich import MpichEnvironmentModifications


class CrayMvapich2(MpichEnvironmentModifications, Package):
    """Cray/HPE packaging of MVAPICH2 for HPE Apollo systems"""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False  # Skip attempts to fetch source that is not available

    maintainers("hppritcha")

    version("8.1.0")
    version("8.0.16")
    version("8.0.14")
    version("8.0.11")
    version("8.0.9")
    version("7.7.16")
    version("7.7.15")
    version("7.7.14")
    version("7.7.13")

    provides("mpi@3")

    requires("platform=linux", msg="Cray MVAPICH2 is only available on Cray")

    def setup_run_environment(self, env):
        env.set("MPICC", self.compiler.cc)
        env.set("MPICXX", self.compiler.cxx)
        env.set("MPIFC", self.compiler.fc)
        env.set("MPIF77", self.compiler.f77)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
