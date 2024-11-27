# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStatmod(RPackage):
    """Statistical Modeling.

    A collection of algorithms and functions to aid statistical modeling.
    Includes limiting dilution analysis (aka ELDA), growth curve comparisons,
    mixed linear models, heteroscedastic regression, inverse-Gaussian
    probability calculations, Gauss quadrature and a secure convergence
    algorithm for nonlinear models. Also includes advanced generalized linear
    model functions including Tweedie and Digamma distributional families and a
    secure convergence algorithm."""

    cran = "statmod"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.5.0", sha256="d61c3ef9b09d55b42e038f8d767fa483ebbdec2a9c7172b1b0ccda0ae0016ec9")
    version("1.4.37", sha256="90d2c8a79e0cb291f2685686436bcf4c5b9abd2efb84759a8553d1b1adb76913")
    version("1.4.36", sha256="14e897c83d426caca4d920d3d5bead7ae9a679276b3cb2e227f299ad189d7bc2")
    version("1.4.35", sha256="de5e428f81c306849af47b9ae583362855e166b1da62893734f1154cb5b3f8fe")
    version("1.4.32", sha256="2f67a1cfa66126e6345f8a40564a3077d08f1748f17cb8c8fb05c94ed0f57e20")
    version("1.4.30", sha256="9d2c1722a85f53623a9ee9f73d835119ae22ae2b8ec7b50d675401e314ea641f")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"))
