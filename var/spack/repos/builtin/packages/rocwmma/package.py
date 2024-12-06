# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack.package import *


class Rocwmma(CMakePackage):
    """AMD's C++ library for accelerating mixed precision matrix multiplication
    and accumulation (MFMA) operations leveraging specialized GPU matrix cores.
    rocWMMA provides a C++ API to facilitate breaking down matrix multiply-accumulate
    problems into fragments and using them in block-wise operations that are
    distributed in parallel across GPU wavefronts. The API is a header library
    of GPU device code meaning that matrix core acceleration may be compiled directly
    into your kernel device code. This can benefit from compiler optimization in the
    generation of kernel assembly, and does not incur additional overhead costs of
    linking to external runtime libraries or having to launch separate kernels."""

    homepage = "https://github.com/ROCm/rocWMMA"
    git = "https://github.com/ROCm/rocWMMA.git"
    url = "https://github.com/ROCm/rocWMMA/archive/refs/tags/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("srekolam", "renjithravindrankannath")
    version("6.2.1", sha256="f05fcb3612827502d2a15b30f0e46228625027145013652b8f591ad403fa9ddc")
    version("6.2.0", sha256="08c5d19f0417ee9ba0e37055152b22f64ed0eab1d9ab9a7d13d46bf8d3b255dc")
    version("6.1.2", sha256="7f6171bea5c8b7cdaf5c64dbfb76eecf606f2d34e8409153a74b56027c5e92a7")
    version("6.1.1", sha256="6e0c15c78feb8fb475ed028ed9b0337feeb45bfce1e206fe5f236a55e33f6135")
    version("6.1.0", sha256="ca29f33cfe6894909159ad68d786eacd469febab33883886a202f13ae061f691")
    version("6.0.2", sha256="61c6cc095b4ac555f4be4b55f6a7e3194c8c54bffc57bfeb0c02191119ac5dc8")
    version("6.0.0", sha256="f9e97e7c6c552d43ef8c7348e4402bead2cd978d0f81a9657d6a0f6c83a6139b")
    version("5.7.1", sha256="a998a1385e6ad7062707ddb9ff82bef727ca48c39a10b4d861667024e3ffd2a3")
    version("5.7.0", sha256="a8f1b090e9e504a149a924c80cfb6aca817359b43833a6512ba32e178245526f")
    version("5.6.1", sha256="41a5159ee1ad5fc411fe6220f37bd754e26d3883c24c0f2378f50ef628bc1b8f")
    version("5.6.0", sha256="78b6ab10fce71d10a9d762b2eaab3390eb13b05c764f47a3b0a303ec3d37acf8")
    version("5.5.1", sha256="ada30d5e52df5da0d3f4e212a25efb492dbedc129628f4db4ef4ed77667da228")
    version("5.5.0", sha256="b9e1938cba111eeea295414c42de34d54a878f0d41a26e433809d60c12d31dbf")
    with default_args(deprecated=True):
        version("5.4.3", sha256="0968366c83b78a9d058d483be536aba03e79b300ccb6890d3da43298be54c288")
        version("5.4.0", sha256="a18724c3b45d171e54ef9f85c269124ce8d29b6a2f9dbd76a4806bda2933f7a7")
        version("5.3.3", sha256="cd9bc09f98fb78e53ba4bde1dcfe1817c34c2822234a82b1128d36d92b97ae79")
        version("5.3.0", sha256="04bac641ba18059118d3faa5f21fe3bf3e285055d40930489ebf27ffc8e5d16e")

    depends_on("cxx", type="build")  # generated

    # gfx908:xnack-;gfx90a:xnack-;gfx90a:xnack+
    # are only targets currently supported for @5.2.0
    # releases

    amdgpu_targets = ("gfx908:xnack-", "gfx90a", "gfx90a:xnack-", "gfx90a:xnack+")
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build", when="@5.2.0:")
    depends_on("cmake@3.5:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on("rocm-cmake@%s:" % ver, type="build", when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, type="build", when="@" + ver)
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("rocblas@" + ver, type="build", when="@" + ver)
        depends_on("rocm-openmp-extras@" + ver, type="build", when="@" + ver)

    for ver in [
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on("rocm-smi-lib@" + ver, when="@" + ver)

    for tgt in itertools.chain(["auto"], amdgpu_targets):
        depends_on("rocblas amdgpu_target={0}".format(tgt), when="amdgpu_target={0}".format(tgt))

    patch("0001-add-rocm-smi-lib-path-for-building-tests.patch", when="@5.6:")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("ROCWMMA_BUILD_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_VALIDATION_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_BENCHMARK_TESTS", "ON"),
            self.define("ROCWMMA_BUILD_SAMPLES", "ON"),
            self.define("ROCWMMA_BUILD_DOCS", "OFF"),
            self.define("ROCWMMA_BUILD_ASSEMBLY", "OFF"),
        ]
        args.extend(
            [
                "-DOpenMP_CXX_FLAGS=-fopenmp=libomp",
                "-DOpenMP_CXX_LIB_NAMES=libomp",
                "-DOpenMP_libomp_LIBRARY={0}/lib/libomp.so".format(
                    self.spec["rocm-openmp-extras"].prefix
                ),
            ]
        )
        tgt = self.spec.variants["amdgpu_target"]
        if "auto" not in tgt:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))
        if self.spec.satisfies("@5.6.0:"):
            args.append(self.define("ROCM_SMI_DIR", self.spec["rocm-smi-lib"].prefix))

        return args
