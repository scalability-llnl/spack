# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.build_systems.cmake
import spack.build_systems.generic
from spack.package import *


class Nekrs(Package, CMakePackage, CudaPackage, ROCmPackage):
    """nekRS is an open-source Navier Stokes solver based on the spectral
    element method targeting classical processors and hardware accelerators
    like GPUs"""

    homepage = "https://github.com/Nek5000/nekRS"
    git = "https://github.com/Nek5000/nekRS.git"
    url = "https://github.com/Nek5000/nekRS/archive/refs/tags/v23.0.tar.gz"

    tags = [
        "cfd",
        "flow",
        "hpc",
        "solver",
        "navier-stokes",
        "spectral-elements",
        "fluid",
        "ecp",
        "ecp-apps",
    ]

    maintainers("thilinarmtb", "stgeke")

    license("BSD-3-Clause")

    build_system(
        conditional("cmake", when="@23.0:"), conditional("generic", when="@=21.0"), default="cmake"
    )

    version("23.0", sha256="2cb4ded69551b9614036e1a9d5ac54c8535826eae8f8b6a00ddb89043b2c392a")
    version("21.0", tag="v21.0", commit="bcd890bf3f9fb4d91224c83aeda75c33570f1eaa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("opencl", default=False, description="Activates support for OpenCL")

    # Conflicts:
    # nekrs includes following packages, but in order to build as part of
    # CEED we can't leave them in as conflicts. They should be enabled
    # sometime in future.
    # for pkg in ['occa', 'hyper', 'nek5000', 'blas', 'lapack', 'gslib']:
    #     conflicts('^' + pkg, msg=(pkg + " is built into nekRS"))

    # Dependencies
    depends_on("mpi")
    depends_on("git")
    depends_on("cmake")

    def patch(self):
        with working_dir("scripts"):
            # Make sure nekmpi wrapper uses srun when we know OpenMPI
            # is not built with mpiexec
            if self.spec.satisfies("^openmpi~legacylaunchers"):
                filter_file(r"mpirun -np", "srun -n", "nrsmpi")
                filter_file(r"mpirun -np", "srun -n", "nrspre")
                filter_file(r"mpirun -np", "srun -n", "nrsbmpi")

    def setup_run_environment(self, env):
        # The 'env' is included in the Spack generated module files.
        spec = self.spec
        env.set("OCCA_CXX", self.compiler.cxx)

        cxxflags = spec.compiler_flags["cxxflags"]
        if cxxflags:
            # Run-time compiler flags:
            env.set("OCCA_CXXFLAGS", " ".join(cxxflags))

        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            # Run-time CUDA compiler:
            env.set("OCCA_CUDA_COMPILER", join_path(cuda_dir, "bin", "nvcc"))


class SetupEnvironment:
    def _setup_runtime_flags(self, s_env):
        spec = self.spec
        s_env.set("OCCA_CXX", self.pkg.compiler.cxx)

        cxxflags = spec.compiler_flags["cxxflags"]
        if cxxflags:
            # Run-time compiler flags:
            s_env.set("OCCA_CXXFLAGS", " ".join(cxxflags))

        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            # Run-time CUDA compiler:
            s_env.set("OCCA_CUDA_COMPILER", join_path(cuda_dir, "bin", "nvcc"))

    def setup_build_environment(self, env):
        spec = self.spec
        # The environment variable CXX is automatically set to the Spack
        # compiler wrapper.

        # The cxxflags, if specified, will be set by the Spack compiler wrapper
        # while the environment variable CXXFLAGS will remain undefined.
        # We define CXXFLAGS in the environment to tell OCCA to use the user
        # specified flags instead of its defaults. This way the compiler will
        # get the cxxflags twice - once from the Spack compiler wrapper and
        # second time from OCCA - however, only the second one will be seen in
        # the verbose output, so we keep both.
        cxxflags = spec.compiler_flags["cxxflags"]
        if cxxflags:
            env.set("CXXFLAGS", " ".join(cxxflags))

        # For the cuda, openmp, and opencl variants, set the environment
        # variable OCCA_{CUDA,OPENMP,OPENCL}_ENABLED only if the variant is
        # disabled. Otherwise, let OCCA autodetect what is available.

        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            cuda_libs_list = ["libcuda", "libcudart", "libOpenCL"]
            cuda_libs = find_libraries(cuda_libs_list, cuda_dir, shared=True, recursive=True)
            env.set("OCCA_INCLUDE_PATH", cuda_dir.include)
            env.set("OCCA_LIBRARY_PATH", ":".join(cuda_libs.directories))
            env.set("OCCA_CUDA_ENABLED", "1")
        else:
            env.set("OCCA_CUDA_ENABLED", "0")

        env.set("OCCA_OPENCL_ENABLED", "1" if "+opencl" in spec else "0")
        env.set("OCCA_HIP_ENABLED", "1" if "+rocm" in spec else "0")

        # Setup run-time environment for testing.
        env.set("OCCA_VERBOSE", "1")
        self._setup_runtime_flags(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self._setup_runtime_flags(env)


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        makenrs = Executable(os.path.join(os.getcwd(), "makenrs"))

        makenrs.add_default_env("NEKRS_INSTALL_DIR", prefix)
        makenrs.add_default_env("NEKRS_CC", spec["mpi"].mpicc)
        makenrs.add_default_env("NEKRS_CXX", spec["mpi"].mpicxx)
        makenrs.add_default_env("NEKRS_FC", spec["mpi"].mpifc)
        makenrs.add_default_env("TRAVIS", "true")

        makenrs(output=str, error=str, fail_on_error=True)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        cxxflags = self.spec.compiler_flags["cxxflags"]
        args = [
            self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
            self.define("NEKRS_COMPILER_FLAGS", cxxflags),
            self.define("OCCA_CXXFLAGS", cxxflags),
            self.define_from_variant("ENABLE_CUDA", "cuda"),
            self.define_from_variant("ENABLE_OPENCL", "opencl"),
            self.define_from_variant("ENABLE_HIP", "rocm"),
        ]
        return args
