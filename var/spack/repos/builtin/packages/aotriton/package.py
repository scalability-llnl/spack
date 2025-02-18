# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Aotriton(CMakePackage):
    """Ahead of Time (AOT) Triton Math Library."""

    homepage = "https://github.com/ROCm/aotriton"
    git = "https://github.com/ROCm/aotriton.git"
    url = "https://github.com/ROCm/aotriton/archive/refs/tags/0.8.2b.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version(
        "0.8.2b", tag="0.8.2b", commit="b24f43a9771622faa157155568b9a200c3b49e41", submodules=True
    )
    version(
        "0.8.1b", tag="0.8.1b", commit="3a80554a88ae3b1bcf4b27bc74ad9d7b913b58f6", submodules=True
    )
    version("0.8b", tag="0.8b", commit="6f8cbcac8a92775291bb1ba8f514d4beb350baf4", submodules=True)

    generator("ninja")
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-filelock", type=("build", "run"))

    depends_on("cmake@3.26:", type="build")
    depends_on("python", type="build")
    depends_on("z3", type="link")
    depends_on("zlib-api", type="link")
    depends_on("xz", type="link")
    depends_on("pkgconfig", type="build")
    conflicts("^openssl@3.3.0")

    # ROCm dependencies
    depends_on("hip", type="build")
    depends_on("llvm-amdgpu", type="build")
    depends_on("comgr", type="build")
    depends_on("hsa-rocr-dev", type="build")

    def patch(self):
        if self.spec.satisfies("^hip"):
            filter_file(
                "/opt/rocm/llvm/bin/ld.lld",
                f'{self.spec["llvm-amdgpu"].prefix}/bin/ld.lld',
                "third_party/triton/third_party/amd/backend/compiler.py",
                string=True,
            )

    def setup_build_environment(self, env):
        """Set environment variables used to control the build"""
        if self.spec.satisfies("%clang"):
            env.set("TRITON_HIP_LLD_PATH", self.spec["llvm-amdgpu"].prefix / bin / ld.lld)

    def cmake_args(self):
        args = []
        args.append(self.define("AOTRITON_GPU_BUILD_TIMEOUT", 0))
        return args
