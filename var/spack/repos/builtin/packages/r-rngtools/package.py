# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRngtools(RPackage):
    """Utility Functions for Working with Random Number Generators.

    Provides a set of functions for working with Random Number Generators
    (RNGs). In particular, a generic S4 framework is defined for
    getting/setting the current RNG, or RNG data that are embedded into objects
    for reproducibility. Notably, convenient default methods greatly facilitate
    the way current RNG settings can be changed."""

    cran = "rngtools"

    license("GPL-3.0-only")

    version("1.5.2", sha256="7f8c76ca4c7851b69a86e27be09b02ddc86357f0388659ef8787634682e8a74d")
    version("1.5", sha256="8274873b73f7acbe0ce007e62893bf4d369d2aab8768754a60da46b3f078f575")
    version("1.4", sha256="3aa92366e5d0500537964302f5754a750aff6b169a27611725e7d84552913bce")
    version("1.3.1.1", sha256="99e1a8fde6b81128d0946746c1ef84ec5b6c2973ad843a080098baf73aa3364c")
    version("1.3.1", sha256="763fc493cb821a4d3e514c0dc876d602a692c528e1d67f295dde70c77009e224")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@1.4:")
    depends_on("r-digest", type=("build", "run"))

    depends_on("r-pkgmaker@0.20:", type=("build", "run"), when="@:1.4")
    depends_on("r-stringr", type=("build", "run"), when="@:1.4")
