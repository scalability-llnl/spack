# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Autodiff(CMakePackage, CudaPackage):
    """autodiff is automatic differentiation made easier for C++."""

    homepage = "https://autodiff.github.io"
    url = "https://github.com/autodiff/autodiff/archive/refs/tags/v0.6.4.tar.gz"
    list_url = "https://github.com/autodiff/autodiff/tags"
    git = "https://github.com/autodiff/autodiff.git"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("1.1.2", sha256="86f68aabdae1eed214bfbf0ddaa182c78ea1bb99e4df404efb7b94d30e06b744")
    version("1.1.1", sha256="05aa2a432c83db079efeca1c407166a3f3d190645bd3202da3b6357fb30fc9e1")
    version("1.1.0", sha256="a5489bb546c460af52de8ead447439b3c97429184df28b4d142ce7dcfd62b82c")
    version("1.0.3", sha256="21b57ce60864857913cacb856c3973ae10f7539b6bb00bcc04f85b2f00db0ce2")
    version("1.0.2", sha256="a3289aed937a39a817f76e6befa0d071a3e70a5b0b125ec62d1acf1d389e2197")
    version("1.0.1", sha256="63f2c8aaf940fbb1d1e7098b1d6c08794da0194eec3faf773f3123dc7233838c")
    version("1.0.0", sha256="112c6f5740071786b3f212c96896abc2089a74bca16b57bb46ebf4cec79dca43")
    version("0.6.12", sha256="3e9d667b81bba8e43bbe240a0321e25f4be248d1761097718664445306882dcc")
    version("0.6.11", sha256="ac7a52387a10ecb8ba77ce5385ffb23893ff9a623467b4392bd204422a3b5c09")
    version("0.6.10", sha256="d6bc2f44cab5fd132deabdcb2a9e914b4959660c80a40a2c3f20dde79fc113d9")
    version("0.6.9", sha256="eae26c9dcd8b423ebcecd1a65365c2af2be80cb6cd273602787900939626a961")
    version("0.6.8", sha256="680fc476ed218a3a0eeb0de017d427921189b50c99e1c509395f10957627fb1a")
    version("0.6.7", sha256="1345021d74bfd34e74a58d98f4e0e16cc4666b6cd18628af0ba642a6521aadfa")
    version("0.6.6", sha256="2a4498b09da9a223b896a3bbfc9ebcb7c7c0b906b19a25000e6f3b94698d916d")
    version("0.6.5", sha256="252ced0f4e892e9957c67fe8bb1c9edd5636f121a8481abc0a0cec9a4c465484")
    version("0.6.4", sha256="cfe0bb7c0de10979caff9d9bfdad7e6267faea2b8d875027397486b47a7edd75")
    version("0.5.13", sha256="a73dc571bcaad6b44f74865fed51af375f5a877db44321b5568d94a4358b77a1")

    depends_on("cxx", type="build")

    variant("python", default=False, description="Enable the compilation of the python bindings.")
    variant("examples", default=False, description="Enable the compilation of the example files.")

    depends_on("cmake@3.0:", type="build")
    depends_on("cmake@3.22:", when="@0.6.8", type="build")
    depends_on("cmake@3.16:", when="@0.6.9:", type="build")
    depends_on("eigen")
    depends_on("py-pybind11", type=("build", "run"))
    depends_on("catch2", type="test")
    depends_on("catch2@3:", when="@0.6.12:", type="test")

    conflicts("+cuda", when="@:1.0", msg="CUDA support was added in 1.1.0")

    def cmake_args(self):
        args = [
            self.define("AUTODIFF_BUILD_TESTS", self.run_tests),
            self.define_from_variant("AUTODIFF_BUILD_PYTHON", "python"),
            self.define_from_variant("AUTODIFF_BUILD_EXAMPLES", "examples"),
        ]
        return args
