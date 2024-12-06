# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    maintainers("pnavaro", "freifrauvonbleifrei")

    version("main", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

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
    depends_on("fftw")
    depends_on("fftw+openmp", when="+openmp")
    depends_on("fgsl")
    depends_on("git", type=("build", "run", "test"))
    depends_on("hdf5+fortran+cxx")
    depends_on("lapack", when="~mpi")
    with when("+mpi"):
        depends_on("mpi")
        depends_on("fftw+mpi")
        depends_on("hdf5+mpi")
        depends_on("scalapack")
    depends_on("python@3.0.0:", type=("build"))
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

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def quick_serial_ctest(self):
        """quickly run a serial subset of tests for sanity check"""
        ctest = which("ctest")
        with working_dir(self.build_directory):
            ctest("--output-on-failure", "-R", "test_mud2")
            ctest("--output-on-failure", "-R", "sparse_grid_4d")
            ctest("--output-on-failure", "-R", "scalar_field_2d")
            ctest("--output-on-failure", "-R", "maxwell_3d_fem_fft")
