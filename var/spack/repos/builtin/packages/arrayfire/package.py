# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "https://arrayfire.org/docs/index.htm"
    git = "https://github.com/arrayfire/arrayfire.git"
    maintainers("umar456")

    license("FreeImage")

    version("master")
    version("3.8.1", commit="823e8e399fe8c120c6ec7ec75f09e6106b3074ca", tag="v3.8.1")
    version(
        "3.7.3", commit="59ac7b980d1ae124aae914fb29cbf086c948954d", submodules=True, tag="v3.7.3"
    )
    version(
        "3.7.2", commit="218dd2c99300e77496239ade76e94b0def65d032", submodules=True, tag="v3.7.2"
    )
    version(
        "3.7.0", commit="fbea2aeb6f7f2d277dcb0ab425a77bb18ed22291", submodules=True, tag="v3.7.0"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("forge", default=False, description="Enable graphics library")
    variant("opencl", default=False, description="Enable OpenCL backend")

    depends_on("boost@1.70:")
    depends_on("fftw-api@3:")
    depends_on("blas")
    depends_on("cuda@7.5:", when="+cuda")
    depends_on("cudnn", when="+cuda")

    depends_on("opencl", when="+opencl")
    depends_on("pocl+icd", when="^[virtuals=opencl] pocl")

    # TODO add more opencl backends:
    # currently only Cuda backend is enabled
    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux#opencl-backend-dependencies

    depends_on("fontconfig", when="+forge")
    depends_on("glfw@3.1.4:", when="+forge")

    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        libraries = []
        if "cpu" in query_parameters:
            libraries.append("libafcpu")
        if "cuda" in query_parameters and "+cuda" in self.spec:
            libraries.append("libafcuda")
        if "opencl" in query_parameters and "+opencl" in self.spec:
            libraries.append("libafopencl")
        if not query_parameters or "unified" in query_parameters:
            libraries.append("libaf")

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def cmake_args(self):
        args = []
        args.extend(
            [
                self.define_from_variant("AF_BUILD_CUDA", "cuda"),
                self.define_from_variant("AF_BUILD_FORGE", "forge"),
                self.define_from_variant("AF_BUILD_OPENCL", "opencl"),
                self.define("BUILD_TESTING", self.run_tests),
            ]
        )

        if self.spec.satisfies("+cuda"):
            arch_list = [
                "{}.{}".format(arch[:-1], arch[-1])
                for arch in self.spec.variants["cuda_arch"].value
            ]
            args.append(self.define("CUDA_architecture_build_targets", arch_list))

        if self.spec["blas"].name in INTEL_MATH_LIBRARIES:
            if self.version >= Version("3.8.0"):
                args.append(self.define("AF_COMPUTE_LIBRARY", "Intel-MKL"))
            else:
                args.append(self.define("USE_CPU_MKL", True))
                args.append(self.define("USE_OPENCL_MKL", True))
            if "%intel" not in self.spec:
                args.append(self.define("MKL_THREAD_LAYER", "GNU OpenMP"))
        else:
            if self.version >= Version("3.8.0"):
                args.append(self.define("AF_COMPUTE_LIBRARY", "FFTW/LAPACK/BLAS"))
            else:
                args.append(self.define("USE_CPU_MKL", False))
                args.append(self.define("USE_OPENCL_MKL", False))

        return args
