# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sleef(CMakePackage):
    """SIMD Library for Evaluating Elementary Functions, vectorized libm and DFT."""

    homepage = "https://sleef.org"
    url = "https://github.com/shibatch/sleef/archive/3.7.tar.gz"
    git = "https://github.com/shibatch/sleef.git"

    maintainers("blapie")

    license("BSL-1.0")

    version("master", branch="master")
    version("3.7.0", commit="c5494730bf601599a55f4e77f357b51ba590585e", preferred=True)
    version("3.6.1", commit="6ee14bcae5fe92c2ff8b000d5a01102dab08d774")
    version("3.6.0_2024-03-20", commit="60e76d2bce17d278b439d9da17177c8f957a9e9b")  # py-torch@2.4:
    version("3.6.0", commit="a99491afee2bae0b11e9ffbf3211349f43a5fd10")
    version(
        "3.5.1_2020-12-22", commit="e0a003ee838b75d11763aa9c3ef17bf71a725bff"
    )  # py-torch@1.8:2.3
    version("3.5.1", sha256="415ee9b1bcc5816989d3d4d92afd0cd3f9ee89cbd5a33eb008e69751e40438ab")
    version(
        "3.4.0_2019-07-30", commit="7f523de651585fe25cade462efccca647dcc8d02"
    )  # py-torch@1.3:1.7
    version(
        "3.4.0_2019-05-13",
        commit="9b249c53a80343cc1a394ca961d7d5696ea76409",  # py-torch@1.2
        git="https://github.com/zdevito/sleef.git",
        deprecated=True,
    )
    version(
        "3.3.1_2018-12-09",
        commit="191f655caa25526ae226cf88dd2529265176014a",  # py-torch@1.1
        git="https://github.com/zdevito/sleef.git",
        deprecated=True,
    )
    version(
        "3.2.0_2018-05-09", commit="6ff7a135a1e31979d1e1844a2e7171dfbd34f54f", deprecated=True
    )  # py-torch@0.4.1:1.0
    version(
        "3.2.0",
        sha256="3130c5966e204e6d6a3ace81e543d12b5b21f60897f1c185bfa587c1bd77bee2",
        deprecated=True,
    )

    depends_on("c", type="build")

    generator("ninja")
    depends_on("cmake@3.18:", type="build")

    depends_on("fftw-api", type="test")
    depends_on("mpfr", type="test")
    depends_on("openssl", type="test")

    # https://github.com/shibatch/sleef/issues/458
    # https://github.com/shibatch/sleef/pull/471
    conflicts("^mpfr@4.2:", when="@:3.5.1_2023-11-20")

    def sleef_define(self, cmake_var, value):
        # https://github.com/shibatch/sleef/pull/509
        if self.spec.satisfies("@3.5.1_2024-02-07:"):
            cmake_var = "SLEEF_" + cmake_var

        return self.define(cmake_var, value)

    def cmake_args(self):
        args = [
            self.sleef_define("BUILD_TESTS", self.run_tests),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]

        # https://github.com/shibatch/sleef/issues/474
        if self.spec.satisfies("@:3.5.1_2024-02-08 platform=darwin"):
            args.append(self.sleef_define("DISABLE_SVE", True))

        return args
