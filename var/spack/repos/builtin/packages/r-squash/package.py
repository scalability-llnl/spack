# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSquash(RPackage):
    """Color-Based Plots for Multivariate Visualization.

    Functions for color-based visualization of multivariate data, i.e.
    colorgrams or heatmaps. Lower-level functions map numeric values to colors,
    display a matrix as an array of colors, and draw color keys. Higher-level
    plotting functions generate a bivariate histogram, a dendrogram aligned
    with a color-coded matrix, a triangular distance matrix, and more."""

    cran = "squash"

    license("Artistic-2.0")

    version("1.0.9", sha256="ff381c85071e3407574e3db28d789657f64e7d3f9d74ac123539de22ab8ac6f4")
    version("1.0.8", sha256="e6932c0a461d5c85f7180a31d18a3eb4f28afd6769efe251075a4de12de039f4")
    version("1.0.7", sha256="d2d7182a72dfd93b8b65e775bea11e891c38598fa49a3ed4f92ec1159ffab6f1")
