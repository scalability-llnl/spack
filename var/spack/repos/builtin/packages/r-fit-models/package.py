# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFitModels(RPackage):
    """Compare Fitted Models.

    The fit.models function and its associated methods (coefficients, print,
    summary, plot, etc.) were originally provided in the robust package to
    compare robustly and classically fitted model objects. See chapters 2, 3,
    and 5 in Insightful (2002) 'Robust Library User's Guide'
    <https://robust.r-forge.r-project.org/Robust.pdf>). The aim of the
    fit.models package is to separate this fitted model object comparison
    functionality from the robust package and to extend it to support fitting
    methods (e.g., classical, robust, Bayesian, regularized, etc.) more
    generally."""

    cran = "fit.models"

    version("0.64", sha256="f70806bfa85a05337fa5a665264d640e307584714a07a329fbe96c86b0e864da")
    version("0.5-14", sha256="93b9d119e97b36c648a19c891fc5e69f5306eb5b9bac16bf377555057afd4b6e")
    version("0.5-13", sha256="7df545fce135159e9abf0a19076628d3ec2999e89f018e142a7a970428823d48")

    depends_on("r-lattice", type=("build", "run"))
