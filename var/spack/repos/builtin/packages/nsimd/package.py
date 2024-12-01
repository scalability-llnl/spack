# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Nsimd(CMakePackage):
    """NSIMD is a vectorization library that abstracts SIMD programming.
    It was designed to exploit the maximum power of processors
    at a low development cost.
    """

    homepage = "https://agenium-scale.github.io/nsimd/"
    url = "https://github.com/agenium-scale/nsimd/archive/v1.0.tar.gz"

    maintainers("eschnett")

    license("MIT")

    version("3.0.1", sha256="6a90d7ce5f9da5cfac872463951f3374bb0e0824d92f714db0fd4901b32497fd")
    version("3.0", sha256="5cab09020ce3a6819ddb3b3b8cafa6bc1377821b596c0f2954f52c852d092d5c")
    version("2.2", sha256="7916bec6c8ea9ddc690a5bfc80fb1b9402f9e1b2a4b4bb6b6bb8eb5a07eb018e")
    version("2.1", sha256="3274f1061d1fac170130b8c75378a6b94580629b3dc1d53db244b51500ee4695")
    # Version 2.0 is disabled since it does not support cmake
    # version('2.0', sha256='b239e98316f93257161b25c8232634884edcee358982a74742981cc9b68da642')
    version("1.0", sha256="523dae83f1d93eab30114321f1c9a67e2006a52595da4c51f121ca139abe0857")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "simd",
        default="auto",
        description="SIMD instruction set",
        values=(
            "auto",
            "CPU",
            "SSE2",
            "SSE42",
            "AVX",
            "AVX2",
            "AVX512_KNL",
            "AVX512_SKYLAKE",
            "NEON128",
            "AARCH64",
            "SVE",
            conditional("SVE128", "SVE256", "SVE512", "SVE1024", "SVE2048", when="@2:"),
            conditional("VMX", "VSX", when="@3:"),
            conditional("CUDA", "ROCM", when="@2:"),
        ),
        multi=False,
    )
    variant(
        "optionals",
        values=any_combination_of("FMA", "FP16"),
        when="@:1",
        description="Optional SIMD features",
    )

    # Requires a C++14 compiler for building.
    # The C++ interface requires a C++11 compiler to use.
    depends_on("cmake@2.8.7:", type="build")
    depends_on("cmake@3.0.2:", type="build", when="@2:")
    # We need `collections.MutableMapping`, which was removed in
    # Python 3.10; see
    # <https://docs.python.org/3.9/library/collections.html>
    depends_on("python@3.0:3.9", type="build")
    depends_on("py-chardet", type="build", when="@3:")
    depends_on("py-requests", type="build", when="@3:")
    depends_on("py-urllib3", type="build", when="@3:")

    @run_before("cmake")
    def generate_code(self):
        """Auto-generates code in the build directory"""
        spec = self.spec
        if self.spec.satisfies("@:1"):
            options = ["egg/hatch.py", "--all", "--force"]
            python = spec["python"].command
            python(*options)

    def cmake_args(self):
        # Required SIMD argument
        simd = self.spec.variants["simd"].value
        if simd == "auto":
            # x86
            if "avx512" in self.spec.target:
                simd = "AVX512_SKYLAKE"
            elif self.spec.satisfies("target=mic_knl"):
                simd = "AVX512_KNL"
            elif "avx2" in self.spec.target:
                simd = "AVX2"
            elif "avx" in self.spec.target:
                simd = "AVX"
            elif "sse4_2" in self.spec.target:
                simd = "SSE42"
            elif "sse2" in self.spec.target:
                simd = "SSE2"
            # ARM
            elif "sve" in self.spec.target:
                # We require an explicit choice for particluar bit widths
                simd = "SVE"
            elif self.spec.satisfies("target=aarch64:"):
                simd = "AARCH64"
            elif "neon" in self.spec.target:
                simd = "NEON128"
            # POWER
            elif "vsx" in self.spec.target:
                simd = "VSX"
            elif self.spec.satisfies("target=ppc64:") or self.spec.satisfies("target=ppc64le:"):
                simd = "VMX"
            # Unknown CPU architecture
            else:
                simd = "CPU"

        if self.spec.satisfies("@:1"):
            cmake_args = ["-DSIMD={0}".format(simd)]
        else:
            cmake_args = ["-Dsimd={0}".format(simd)]

        if self.spec.satisfies("@:1"):
            # Optional SIMD instructions to be turned on explicitly
            optionals_value = self.spec.variants["optionals"].value
            if optionals_value != "none":
                optionals_arg = ";".join(optionals_value)
                cmake_args.append("-DSIMD_OPTIONALS={0}".format(optionals_arg))

        return cmake_args
