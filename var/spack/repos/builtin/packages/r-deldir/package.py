# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDeldir(RPackage):
    """Delaunay Triangulation and Dirichlet (Voronoi) Tessellation.

    Calculates the Delaunay triangulation and the Dirichlet or Voronoi
    tessellation (with respect to the entire plane) of a planar point set.
    Plots triangulations and tessellations in various ways. Clips tessellations
    to sub-windows. Calculates perimeters of tessellations.  Summarises
    information about the tiles of the tessellation."""

    cran = "deldir"

    license("GPL-2.0-or-later")

    version("2.0-4", sha256="d418acb28ec3707b6d64c7466d0cefbb49b098537f37558d8f7a5befd34a4653")
    version("1.0-6", sha256="6df6d8325c607e0b7d63cbc53c29e774eff95ad4acf9c7ec8f70693b0505f8c5")
    version("0.2-3", sha256="2d24800f5ec6ad9dc57b9b265365b29c07717f4562d8f3e6344336d3340c364e")
    version("0.1-23", sha256="e0112bce9fc94daf73596a0fff9b3958b80872e3bbb487be73e157b13a6f201d")
    version("0.1-21", sha256="b9dabcc1813c7a0f8edaf720a94bdd611a83baf3d3e52e861d352369e815690c")
    version("0.1-14", sha256="89d365a980ef8589971e5d311c6bd59fe32c48dbac8000a880b9655032c99289")

    depends_on("r@0.99:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.2-3:")
