# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REvd(RPackage):
    """Functions for Extreme Value Distributions.

    Extends simulation, distribution, quantile and density functions to
    univariate and multivariate parametric extreme value distributions, and
    provides fitting functions which calculate maximum likelihood estimates for
    univariate and bivariate maxima models, and for univariate and bivariate
    threshold models."""

    cran = "evd"

    license("GPL-3.0-only")

    version("2.3-7", sha256="4a899df15d39be4a8d544de4f5e4690b4673790a46da6a6c9c2a70fef3b55648")
    version("2.3-6.1", sha256="662c592d3f5c5693dbf1c673d1137c4a60a347e330b71be1f3933f201d2c8971")
    version("2.3-6", sha256="8edb8bc4f06d246c4343fd923bb5d5df99724d6db8821bfd996220343a834cb6")
    version("2.3-3", sha256="2fc5ef2e0c3a2a9392425ddd45914445497433d90fb80b8c363877baee4559b4")
