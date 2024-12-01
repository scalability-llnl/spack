# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMscoreutils(RPackage):
    """Core Utils for Mass Spectrometry Data.

    MsCoreUtils defines low-level functions for mass spectrometry data and is
    independent of any high-level data structures. These functions include mass
    spectra processing functions (noise estimation, smoothing, binning),
    quantitative aggregation functions (median polish, robust summarisation,
    ...), missing data imputation, data normalisation (quantiles, vsn, ...) as
    well as misc helper functions, that are used across high-level data
    structure within the R for Mass Spectrometry packages."""

    bioc = "MsCoreUtils"

    version("1.12.0", commit="14a3fdb2fecca41ef0acb67bc8356227a1491c56")
    version("1.10.0", commit="742c0c7143b1c32f75cc96b555e9f8cd265096c9")
    version("1.8.0", commit="8b7e2c31009276aad0b418ba5cdfc94d03e1973e")
    version("1.6.0", commit="9ed95b2d20dacaa83567fadd04349c81db9127ef")

    depends_on("c", type="build")  # generated

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-clue", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
