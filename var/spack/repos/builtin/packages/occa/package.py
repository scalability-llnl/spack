# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Occa(CMakePackage, CudaPackage, ROCmPackage):
    """OCCA is an open-source (MIT license) library used to program current
    multi-core/many-core architectures. Devices (such as CPUs, GPUs,
    Intel's Xeon Phi, FPGAs, etc) are abstracted using an offload-model
    for application development and programming for the devices is done
    through a C-based (OKL) or Fortran-based kernel language (OFL).
    OCCA gives developers the ability to target devices at run-time by
    using run-time compilation for device kernels.
    """

    homepage = "https://libocca.org"
    git = "https://github.com/libocca/occa.git"

    maintainers("v-dobrev", "dmed256")

    license("MIT")

    version("develop")
    version("2.0.0", tag="v2.0.0", commit="3cba0841b2b87678da53e0b311cb7e162d781181")
    version("1.2.0", tag="v1.2.0", commit="18379073b6497f677a20bfeced95b511f82c3355")
    version("1.1.0", tag="v1.1.0", commit="c8a587666a23e045f25dc871c3257364a5f6a7d5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("cmake@3.30:", type="build")  # generated

    variant("opencl", default=True, description="Enable support for OpenCL")
    variant("openmp", default=True, description="Enable support for OpenMP")
    variant("debug", default=False, description="Enable a build with debug symbols")

    conflicts("%gcc@6:", when="^cuda@:8")
    conflicts("%gcc@7:", when="^cuda@:9")

    def cmake_args(self):
        spec = self.spec
        args, include_dirs, library_dirs = [], [], []

        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            cuda_libs_list = ["libcuda", "libcudart", "libOpenCL"]
            cuda_libs = find_libraries(cuda_libs_list, cuda_dir, shared=True, recursive=True)
            include_dirs.append(cuda_dir.include)
            library_dirs.extend(cuda_libs.directories)
        else:
            args.append("-DOCCA_ENABLE_CUDA=0")

        if "+rocm" in spec:
            hip_dir = spec["hip"].prefix
            hip_libs_list = ["amdhip64"]
            hip_libs = find_libraries(hip_libs_list, hip_dir, shared=True, recursive=True)
            include_dirs.append(hip_dir.include)
            library_dirs.extend(hip_libs.directories)
        else:
            args.append("-DOCCA_ENABLE_HIP=0")

        if "~opencl" in spec:
            args.append("-DOCCA_ENABLE_OPENCL=0")

        if "~openmp" in spec:
            args.append("-DOCCA_ENABLE_OPENMP=0")

        if "+debug" in spec:
            args.append("-DCMAKE_BUILD_TYPE=Debug")

        args.append("-DCMAKE_INCLUDE_PATH={0}".format(";".join(include_dirs)))
        args.append("-DCMAKE_LIBRARY_PATH={0}".format(";".join(library_dirs)))

        return args

    def _setup_runtime_flags(self, s_env):
        spec = self.spec
        s_env.set("OCCA_DIR", self.prefix)
        s_env.set("OCCA_CXX", self.compiler.cxx)

        # Run-time compiler flags:
        cxxflags = spec.compiler_flags["cxxflags"]
        if cxxflags:
            s_env.set("OCCA_CXXFLAGS", " ".join(cxxflags))

        # Setup run-time HIP/CUDA compilers:
        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            s_env.set("OCCA_CUDA_COMPILER", join_path(cuda_dir, "bin", "nvcc"))

        if "+rocm" in spec:
            hip_dir = spec["hip"].prefix
            s_env.set("OCCA_HIP_COMPILER", join_path(hip_dir, "bin", "hipcc"))

    def _setup_build_flags(self, env):
        # Setup run-time environment for testing.
        env.set("OCCA_VERBOSE", "1")
        self._setup_runtime_flags(env)

    def setup_build_environment(self, env):
        self._setup_build_flags(env)

    def setup_run_environment(self, env):
        # The 'env' is included in the Spack generated module files.
        self._setup_runtime_flags(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self._setup_runtime_flags(env)

    @run_after("install")
    def check_install(self):
        version_cmd = join_path(self.prefix.bin, "occa") + " version"
        val = os.system(version_cmd)
        if val != 0:
            raise RuntimeError("Calling `occa version` failed !")
