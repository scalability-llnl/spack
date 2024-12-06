# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDiagram(RPackage):
    """Functions for Visualising Simple Graphs (Networks), Plotting Flow
    Diagrams.

    Visualises simple graphs (networks) based on a transition matrix, utilities
    to plot flow diagrams, visualising webs, electrical networks, etc. Support
    for the book "A practical guide to ecological modelling - using R as a
    simulation platform" by Karline Soetaert and Peter M.J. Herman (2009),
    Springer. and the book "Solving Differential Equations in R" by Karline
    Soetaert, Jeff Cash and Francesca Mazzia (2012), Springer. Includes
    demo(flowchart), demo(plotmat), demo(plotweb)."""

    cran = "diagram"

    license("GPL-2.0-or-later")

    version("1.6.5", sha256="e9c03e7712e0282c5d9f2b760bafe2aac9e99a9723578d9e6369d60301f574e4")

    depends_on("r@2.1:", type=("build", "run"))
    depends_on("r-shape", type=("build", "run"))
