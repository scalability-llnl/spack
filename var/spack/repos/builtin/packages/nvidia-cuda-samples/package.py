# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
from spack.package import *

class NvidiaCudaSamples(CMakePackage, MakefilePackage, CudaPackage):
    """A collection of NVIDIA curated sample applications showcasing features of CUDA"""

    homepage = "https://github.com/NVIDIA/cuda-samples"
    url = "https://github.com/NVIDIA/cuda-samples"
    git = "https://github.com/NVIDIA/cuda-samples"
    versions = ["12.8", "12.5", "12.4.1", "12.4", "12.3", "12.2", "12.1", "12.0", "11.8", "11.6"]
    maintainers("scothalverson")
    license("NVIDIA Software License Agreement")

    # all versions are tied to a specific version of CUDA
    for v in versions:
        version(v, tag="v" + v)
        depends_on("cuda@" + v, when="@" + v)

    variant("cuda", True, "build using CUDA (required)")
    requires("+cuda")

    # cuda-samples changed build systems starting with 12.8
    build_system(
        conditional("cmake", when="@12.8:"),
        conditional("makefile", when="@:12.5"),
        default="cmake",
    )

    # after the change to CMake, the build defaults to all GPU arches
    # supported by the NVCC it depends on
    conflicts("cuda_arch=none", when="@:12.5+cuda", msg="CUDA architecture is required")

    @when("@:12.5")
    def setup_build_environment(self, env):
        env.set("CUDA_PATH", self.spec["cuda"].prefix)
        env.set("SMS", self.spec.variants["cuda_arch"].value[0])

    @when("@12.8:")
    def cmake_args(self):
        args = ["-DCUDAToolkit_ROOT=" + self.spec["cuda"].prefix]
        return args

    # cuda-samples doesn't actually install the samples in the
    # CMAKE_INSTALL_PREFIX dir, so this copies them
    @when("@12.8:")
    def install(self, spec, prefix):
        short_hash = spec.prefix.split("-")[-1][0:7]
        shutil.copytree("../spack-build-" + short_hash + "/Samples", prefix + "/bin/")

    # similar to the CMake version, the Make version doesn't have an install phase
    # but instead just creates binaries in a `bin` folder under the build directory
    @when("@:12.5")
    def install(self, spec, prefix):
        shutil.copytree("./bin/", prefix + "/bin/")
