# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psimd(CMakePackage):
    """Portable 128-bit SIMD intrinsics."""

    homepage = "https://github.com/Maratyszcza/psimd"
    git = "https://github.com/Maratyszcza/psimd.git"

    license("MIT")

    version("master", branch="master")
    version("2020-05-17", commit="072586a71b55b7f8c584153d223e95687148a900")  # py-torch@1.6:1.9
    version("2019-12-26", commit="10b4ffc6ea9e2e11668f86969586f88bc82aaefa")  # py-torch@1.5
    version("2018-09-06", commit="90a938f30ba414ada2f4b00674ee9631d7d85e19")  # py-torch@1.0:1.4
    version("2017-10-26", commit="4ac61b112252778b174575931c641bef661ab3cd")  # py-torch@0.4

    generator("ninja")
    depends_on("cmake@2.8.12:", type="build")
