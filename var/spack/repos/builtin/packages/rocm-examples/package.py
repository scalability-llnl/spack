# Copyright 2013-2025 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmExamples(CMakePackage):
    """A collection of examples for the ROCm software stack"""

    homepage = "https://github.com/ROCm/rocm-examples"
    url = "https://github.com/ROCm/rocm-examples/archive/refs/tags/rocm-6.2.1.tar.gz"

    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    license("MIT")

    version("6.3.0", sha256="809b5212d86d182586d676752b192967aee3bde6df8bbbe67558b221d63f5c7c")
    version("6.2.4", sha256="510931103e4a40b272123b5c731d2ea795215c6171810beb1d5335d73bcc9b03")
    version("6.2.1", sha256="2e426572aa5f5b44c7893ea256945c8733b79db39cca84754380f40c8b44a563")
    version("6.2.0", sha256="6fb1f954ed32b5c4085c7f071058d278c2e1e8b7b71118ee5e85cf9bbc024df0")

    depends_on("cxx", type="build")

    depends_on("glfw", type="build")

    for ver in ["6.3.0", "6.2.4", "6.2.1", "6.2.0"]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("hipcub@" + ver, when="@" + ver)
        depends_on("hiprand@" + ver, when="@" + ver)
        depends_on("hipsolver@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, when="@" + ver)
        depends_on("rocthrust@" + ver, when="@" + ver)
        depends_on("hipblas@" + ver, when="@" + ver)
        depends_on("rocsparse@" + ver, when="@" + ver)
        depends_on("rocsolver@" + ver, when="@" + ver)

    def patch(self):
        filter_file(
            r"${ROCM_ROOT}/bin/hipify-perl",
            f"{self.spec['hipify-clang'].prefix}/bin/hipify-perl",
            "HIP-Basic/hipify/CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = []
        args.append(
            self.define(
                "OFFLOAD_BUNDLER_COMMAND",
                f"{self.spec['llvm-amdgpu'].prefix}/bin/clang-offload-bundler",
            )
        )
        args.append(
            self.define("LLVM_MC_COMMAND", f"{self.spec['llvm-amdgpu'].prefix}/bin/llvm-mc")
        )
        args.append(
            self.define("LLVM_DIS_COMMAND", f"{self.spec['llvm-amdgpu'].prefix}/bin/llvm-dis")
        )
        return args
