# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fbgemm(CMakePackage):
    """FBGEMM (Facebook GEneral Matrix Multiplication) is a low-precision,
    high-performance matrix-matrix multiplications and convolution library
    for server-side inference."""

    homepage = "https://github.com/pytorch/FBGEMM"
    git = "https://github.com/pytorch/FBGEMM.git"

    maintainers("dskhudia")

    license("BSD-3-Clause")

    version("master", branch="master", submodules=True)
    version(
        "2021-05-10", commit="7794b2950b35ddfa7426091e7fb2f991b1407557", submodules=True
    )  # py-torch@1.9
    version(
        "2020-11-13", commit="9b0131179f293a645bfd3409cd66fa5eecc393b0", submodules=True
    )  # py-torch@1.8
    version(
        "2020-09-14", commit="1d710393d5b7588f5de3b83f51c22bbddf095229", submodules=True
    )  # py-torch@1.7
    version(
        "2020-05-31", commit="7d673046a6a3ad1fa0d15dfb189cd06ffa217041", submodules=True
    )  # py-torch@1.6
    version(
        "2020-05-21", commit="e526aadd058f2a0b8ce738be022e0e4ab4233a2d", submodules=True
    )  # py-torch@1.5.1
    version(
        "2020-03-22", commit="58c002d1593f32aa420ab56b5c344e60d3fb6d05", submodules=True
    )  # py-torch@1.5.0
    version(
        "2019-11-20", commit="399ea148f1403c100e6d601ec3587a621de96a84", submodules=True
    )  # py-torch@1.4
    version(
        "2019-09-26", commit="7dfeddb5ba976f47471275b2468909dfd9b577e1", submodules=True
    )  # py-torch@1.3
    version(
        "2019-07-22", commit="f712cb2328a2b29424bdaeecb9c0731da2cd997b", submodules=True
    )  # py-torch@1.2
    version(
        "2019-04-18", commit="6ec218e6ed5dcb9b5397a608a3b5b8027b236819", submodules=True
    )  # py-torch@1.1
    version(
        "2019-01-23", commit="79333308f5e2fc242727879dcd3de3536b6ffc39", submodules=True
    )  # py-torch@1.0.1
    version(
        "2018-12-04", commit="0d5a159b944252e70a677236b570f291943e0543", submodules=True
    )  # py-torch@1.0.0

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")
    depends_on("llvm-openmp", when="%apple-clang")

    conflicts("%gcc@:4", msg="FBGEMM requires GCC 5+")

    @run_before("cmake")
    def check_requirements(self):
        if "avx2" not in self.spec.target:
            raise RuntimeError(
                "FBGEMM requires a CPU with support for AVX2 instruction set or higher"
            )
