# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdespatial(RPackage):
    """Multivariate Multiscale Spatial Analysis.

    Tools for the multiscale spatial analysis of multivariate data. Several
    methods are based on the use of a spatial weighting matrix and its
    eigenvector decomposition (Moran's Eigenvectors Maps, MEM). Several
    approaches are described in the review Dray et al (2012)
    <doi:10.1890/11-1183.1>."""

    cran = "adespatial"

    license("GPL-2.0-or-later")

    version("0.3-23", sha256="70e0878b13212f9c450bf1e2bd1c5be87a1e24fed942941855a8dd2dd0c05f33")
    version("0.3-21", sha256="4ff65f9bc05892a2d37d34ab2b77dbd24f980adc891f5f94f8e56aec771ea79f")
    version("0.3-20", sha256="f88e009563087c52af5be490bd111cc38b0b70437bbfa189e846080a069b64eb")
    version("0.3-19", sha256="db50f1c42961e40bcef6d714a89a09b1345dab2dd013cea8e2122fdf99d5d223")
    version("0.3-16", sha256="987bd6e0bc6a32ac8e678338ffbbd88580007c4916129b51da681c331818a821")
    version("0.3-14", sha256="a2ef7549c1ed7a23651716c633b25eaff468af8ccbf2e9fcd164e485984cbfbf")
    version("0.3-8", sha256="e3fd3209ce3f0a862a0794187e8c884f1697c87c96e569a2f51f252e00022906")

    depends_on("r-ade4@1.7-13:", type=("build", "run"))
    depends_on("r-adegraphics", type=("build", "run"))
    depends_on("r-adephylo", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-spdep", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"))
    depends_on("r-vegan", type=("build", "run"))
