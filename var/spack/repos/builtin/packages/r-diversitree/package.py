# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RDiversitree(RPackage):
    """Comparative 'Phylogenetic' Analyses of Diversification.

    Mostly focusing on analysing diversification and character evolution.
    Contains implementations of 'BiSSE' (Binary State 'Speciation' and
    Extinction) and its unresolved tree extensions, 'MuSSE' (Multiple State
    'Speciation' and Extinction), 'QuaSSE', 'GeoSSE', and 'BiSSE-ness' Other
    included methods include Markov models of discrete and continuous trait
    evolution and constant rate 'speciation' and extinction."""

    cran = "diversitree"

    license("GPL-2.0-or-later")

    version("0.10-0", sha256="c13627e04bc55b61de218a6bf6fa44680970604f82eed88417d1de5717d782f6")
    version("0.9-16", sha256="4c236970b58e56b922352f3f5d97010c74d8ec5783b375c311fe11abfb99f967")
    version("0.9-15", sha256="c739ef3d4fcc24fd6855b1d297d31e0f89fbaff1efe8a2d149044458ecd363ea")
    version("0.9-11", sha256="4caa6a468f93de9f1c8c30e4457f34bb8346e1acdaf74f684005bfa86a950ecb")
    version("0.9-10", sha256="e7df5910c8508a5c2c2d6d3deea53dd3f947bb762196901094c32a7033cb043e")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-desolve@1.7:", type=("build", "run"))
    depends_on("r-subplex", type=("build", "run"))
    depends_on("r-rcpp@0.10.0:", type=("build", "run"))
    depends_on("fftw@3.1.2:")
    depends_on("gsl@1.15:")
