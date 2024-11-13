# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.build_systems.cmake import CMakeBuilder
from spack.build_systems.makefile import MakefileBuilder
from spack.package import *


class Occa(CMakePackage, MakefilePackage, CudaPackage, ROCmPackage):
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
    version("1.0.9", tag="v1.0.9", commit="ebdb659c804f91f1e0f32fd700f9fe229458033c")
    version("1.0.8", tag="v1.0.8", commit="55264f6b3d426f160dcf1f768c42d16d3ec14676")
    version(
        "1.0.0-alpha.5", tag="v1.0.0-alpha.5", commit="882ed5f92a40e60a80721727c350557be0ce6373"
    )
    version("0.2.0", tag="v0.2.0", commit="2eceaa5706ad6cf3a1b153c1f2a8a2fffa2d5945")
    version("0.1.0", tag="v0.1.0", commit="381e886886dc87823769c5f20d0ecb29dd117afa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("cmake@3.30:", type="build", when="build_system=cmake @1.1.10:")

    build_system(
        conditional("cmake", when="@2.0.0:"),
        conditional("makefile", when="@:1.2.0"),
        default="makefile",
    )

    variant("opencl", default=True, description="Enable support for OpenCL")
    variant("openmp", default=True, description="Enable support for OpenMP")
    variant("debug", default=False, description="Enable a build with debug symbols")

    conflicts("%gcc@6:", when="^cuda@:8")
    conflicts("%gcc@7:", when="^cuda@:9")

    @run_after("install")
    def check_install(self):
        version_cmd = join_path(self.prefix.bin, "occa") + " version"
        val = os.system(version_cmd)
        if val != 0:
            raise RuntimeError("Calling `occa version` failed !")


class SetupEnvironment:
    def setup_run_environment(self, s_env):
        # The 'env' is included in the Spack generated module files.
        spec = self.spec
        s_env.set("OCCA_DIR", self.prefix)
        s_env.set("OCCA_CXX", spack_cxx)

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

    def setup_build_environment(self, env):
        # The environment variable CXX is automatically set to the Spack
        # compiler wrapper.
        # The cxxflags, if specified, will be set by the Spack compiler wrapper
        # while the environment variable CXXFLAGS will remain undefined.
        # We define CXXFLAGS in the environment to tell OCCA to use the user
        # specified flags instead of its defaults. This way the compiler will
        # get the cxxflags twice - once from the Spack compiler wrapper and
        # second time from OCCA - however, only the second one will be seen in
        # the verbose output, so we keep both.
        spec = self.spec
        cxxflags = spec.compiler_flags["cxxflags"]
        if cxxflags:
            env.set("CXXFLAGS", " ".join(cxxflags))

        # Following only apply to the make build.
        # For the cuda, openmp, and opencl variants, set the environment
        # variable OCCA_{CUDA,OPENMP,OPENCL}_ENABLED only if the variant is
        # disabled. Otherwise, let OCCA autodetect what is available.
        if "+cuda" in spec:
            cuda_dir = spec["cuda"].prefix
            cuda_libs_list = ["libcuda", "libcudart", "libOpenCL"]
            cuda_libs = find_libraries(cuda_libs_list, cuda_dir, shared=True, recursive=True)
            env.set("OCCA_INCLUDE_PATH", cuda_dir.include)
            env.set("OCCA_LIBRARY_PATH", ":".join(cuda_libs.directories))
        else:
            env.set("OCCA_CUDA_ENABLED", "0")

        # Disable hip autodetection for now since it fails on some machines.
        env.set("OCCA_HIP_ENABLED", "0")

        if "~opencl" in spec:
            env.set("OCCA_OPENCL_ENABLED", "0")

        if "~openmp" in spec:
            env.set("OCCA_OPENMP_ENABLED", "0")

        # Setup run-time environment for testing.
        env.set("OCCA_VERBOSE", "1")
        self.setup_run_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self.setup_run_environment(env)


class CMakeBuilder(CMakeBuilder, SetupEnvironment):
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


class MakefileBuilder(MakefileBuilder, SetupEnvironment):
    def install(self, pkg, spec, prefix):
        # The build environment is set by the 'setup_build_environment' method.
        # Copy the source to the installation directory and build OCCA there.
        install_tree(".", prefix)
        make("-C", prefix)

        if self.run_tests:
            make("-C", prefix, "test", parallel=False)
