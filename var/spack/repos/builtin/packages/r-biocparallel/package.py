# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocparallel(RPackage):
    """Bioconductor facilities for parallel evaluation.

    This package provides modified versions and novel implementation of
    functions for parallel evaluation, tailored to use with Bioconductor
    objects."""

    bioc = "BiocParallel"

    version("1.34.0", commit="f3bbc0a2d38da034c50ca1e4704fc4ee99a2dc9e")
    version("1.32.1", commit="6c85dbad596a74a6d3022173a4a11c6b81a4a2c2")
    version("1.30.4", commit="1229ebe9f6d8305f9f61e562464f83f9ba86e699")
    version("1.30.2", commit="e7e109f7a94dbfbc50f926be030c7ad8c1a053db")
    version("1.28.3", commit="2f9d88ad83659939e7911d49c2d24d2cd599c7cc")
    version("1.24.1", commit="f713caa4314ec0ddeba7fe0eb599ad417efb413f")
    version("1.18.1", commit="348264af782d7dcd41a1879400f348f836767f6e")
    version("1.16.6", commit="7f7a54c47f4949b600b9fd568289a519496bc4d4")
    version("1.14.2", commit="1d5a44960b19e9dbbca04c7290c8c58b0a7fc299")
    version("1.12.0", commit="2143a9addceed0151a27b95c70aadd2add5cbace")
    version("1.10.1", commit="a76c58cf99fd585ba5ea33065649e68f1afe0a7d")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.5.0:", type=("build", "run"), when="@1.28.3:")
    depends_on("r-futile-logger", type=("build", "run"))
    depends_on("r-snow", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"), when="@1.30.4:")
    depends_on("r-bh", type=("build", "run"), when="@1.12.0:")
    depends_on("r-cpp11", type=("build", "run"), when="@1.32.1:")
