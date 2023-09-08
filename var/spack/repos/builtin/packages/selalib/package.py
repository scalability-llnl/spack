# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Selalib(CMakePackage):
    """SeLaLib is a modular library for the kinetic and gyrokinetic simulation
    of tokamak plasmas by the semi-lagrangian or particle-in-cell methods"""

    homepage = "https://selalib.github.io/selalib"
    url = "https://github.com/selalib/selalib"
    git = "https://github.com/selalib/selalib"

    maintainers = ["pnavaro", "freifrauvonbleifrei"]

    version("main", branch="main")

    variant("fmempool", default=False, description="Use memory pool")
    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=True, description="Build with OpenMP support")
    variant("compression", default=False, description="Add compression by ZFP")

    requires(
        "%gcc@9.0.0:",
        "%clang@16.0.0:",
        "%intel@18.0:",
        "%oneapi@18.0:",
        policy="one_of",
        msg="SeLaLib requires new-enough Fortran compiler",
    )

    depends_on("cmake@3.6.0:", type=("build"))
    depends_on("blas")
    depends_on("fftw+mpi+openmp")
    depends_on("fgsl")
    depends_on("git")
    depends_on("hdf5+fortran+cxx")
    depends_on("mpi+fortran+cxx")
    depends_on("python@3.0.0:")
    # beware: compiling w/ zfp may throw type mismatch errors
    depends_on("zfp+fortran", when="+compression")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP_ENABLED", "openmp"),
            self.define_from_variant("HDF5_PARALLEL_ENABLED", "mpi"),
            self.define_from_variant("USE_FMEMPOOL", "fmempool"),
            self.define("FFTW_ENABLED", "ON"),
        ]
        return args

    def setup_build_environment(self, env):
        env.set("FFTW_INCLUDE", self.spec["fftw"].prefix.include)
        env.set("FFTW_ROOT", self.spec["fftw"].prefix)
