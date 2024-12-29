# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Embree(CMakePackage):
    """Intel Embree High Performance Ray Tracing Kernels"""

    homepage = "https://embree.org"
    url = "https://github.com/embree/embree/archive/v3.7.0.tar.gz"
    maintainers("aumuell")

    license("Apache-2.0")

    version("4.3.3", sha256="8a3bc3c3e21aa209d9861a28f8ba93b2f82ed0dc93341dddac09f1f03c36ef2d")
    version("4.3.2", sha256="dc7bb6bac095b2e7bc64321435acd07c6137d6d60e4b79ec07bb0b215ddf81cb")
    version("4.3.1", sha256="824edcbb7a8cd393c5bdb7a16738487b21ecc4e1d004ac9f761e934f97bb02a4")
    version("4.3.0", sha256="baf0a57a45837fc055ba828a139467bce0bc0c6a9a5f2dccb05163d012c12308")
    version("4.2.0", sha256="b0479ce688045d17aa63ce6223c84b1cdb5edbf00d7eda71c06b7e64e21f53a0")
    version("4.1.0", sha256="117efd87d6dddbf7b164edd94b0bc057da69d6422a25366283cded57ed94738b")
    version("4.0.1", sha256="1fa3982fa3531f1b6e81f19e6028ae8a62b466597f150b853440fe35ef7c6c06")
    version("4.0.0", sha256="bb967241f9516712a9f8e399ed7f756d7baeec3c85c223c0005ede8b95c9fa61")
    version("3.13.5", sha256="b8c22d275d9128741265537c559d0ea73074adbf2f2b66b0a766ca52c52d665b")
    version("3.13.4", sha256="e6a8d1d4742f60ae4d936702dd377bc4577a3b034e2909adb2197d0648b1cb35")
    version("3.13.3", sha256="74ec785afb8f14d28ea5e0773544572c8df2e899caccdfc88509f1bfff58716f")
    version("3.13.2", sha256="dcda827e5b7a606c29d00c1339f1ef00f7fa6867346bc46a2318e8f0a601c6f9")
    version("3.13.1", sha256="00dbd852f19ae2b95f5106dd055ca4b304486436ced0ccf842aec4e38a4df425")
    version("3.13.0", sha256="4d86a69508a7e2eb8710d571096ad024b5174834b84454a8020d3a910af46f4f")
    version("3.12.2", sha256="22a527622497e07970e733f753cc9c10b2bd82c3b17964e4f71a5fd2cdfca210")
    version("3.12.1", sha256="0c9e760b06e178197dd29c9a54f08ff7b184b0487b5ba8b8be058e219e23336e")
    version("3.12.0", sha256="f3646977c45a9ece1fb0cfe107567adcc645b1c77c27b36572d0aa98b888190c")
    version("3.11.0", sha256="2ccc365c00af4389aecc928135270aba7488e761c09d7ebbf1bf3e62731b147d")
    version("3.10.0", sha256="f1f7237360165fb8859bf71ee5dd8caec1fe02d4d2f49e89c11d250afa067aff")
    version("3.9.0", sha256="53855e2ceb639289b20448ae9deab991151aa5f0bc7f9cc02f2af4dd6199d5d1")
    version("3.8.0", sha256="40cbc90640f63c318e109365d29aea00003e4bd14aaba8bb654fc1010ea5753a")
    version("3.7.0", sha256="2b6300ebe30bb3d2c6e5f23112b4e21a25a384a49c5e3c35440aa6f3c8d9fe84")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ispc", default=True, description="Enable ISPC support")
    depends_on("ispc", when="+ispc", type="build")

    depends_on("tbb")

    # official aarch64 support on macOS starting with 3.13.0, on Linux since 4.0.0
    # upstream patch for Linux/aarch64 applies cleanly to 3.13.5, and 3.13.3 works by chance
    conflicts("@:3.12", when="target=aarch64:")
    conflicts("@:3.13.2", when="target=aarch64: platform=linux")
    conflicts("@3.13.4", when="target=aarch64: platform=linux")
    patch(
        "https://github.com/embree/embree/commit/82ca6b5ccb7abe0403a658a0e079926478f04cb1.patch?full_index=1",
        sha256="3af5a65e8875549b4c930d4b0f2840660beba4a7f295d8c89068250a1df376f2",
        when="@3.13.5",
    )

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DBUILD_TESTING=OFF",
            "-DEMBREE_TUTORIALS=OFF",
            "-DEMBREE_IGNORE_CMAKE_CXX_FLAGS=ON",
            self.define_from_variant("EMBREE_ISPC_SUPPORT", "ispc"),
        ]

        if spec.satisfies("target=x86_64:") or spec.satisfies("target=x86:"):
            # code selection and defines controlling namespace names are based on
            # defines controlled by compiler flags, so disable ISAs below compiler
            # flags chosen by spack
            args.append(self.define("EMBREE_ISA_SSE2", "sse4_2" not in spec.target))
            args.append(self.define("EMBREE_ISA_SSE42", "avx" not in spec.target))
            args.append(self.define("EMBREE_ISA_AVX", "avx2" not in spec.target))
            args.append(self.define("EMBREE_ISA_AVX2", "avx512" not in spec.target))

            # during the 3.12 cycle AVX512SKX was renamed to AVX512,
            # but for compatibility, the old name is still supported
            avx512_suffix = ""
            if spec.satisfies("@:3.12"):
                avx512_suffix = "SKX"
            args.append(self.define("EMBREE_ISA_AVX512" + avx512_suffix, True)),
            if spec.satisfies("%gcc@:7"):
                # remove unsupported -mprefer-vector-width=256, otherwise copied
                # from common/cmake/gnu.cmake
                args.append(
                    self.define(
                        "FLAGS_AVX512" + avx512_suffix,
                        "-mavx512f -mavx512dq -mavx512cd -mavx512bw -mavx512vl"
                        " -mf16c -mavx2 -mfma -mlzcnt -mbmi -mbmi2",
                    )
                )

        return args
