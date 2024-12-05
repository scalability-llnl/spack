# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDirichletmultinomial(RPackage):
    """Dirichlet-Multinomial Mixture Model Machine Learning for Microbiome
    Data.

    Dirichlet-multinomial mixture models can be used to describe variability
    in microbial metagenomic data. This package is an interface to code
    originally made available by Holmes, Harris, and Quince, 2012, PLoS ONE
    7(2): 1-15, as discussed further in the man page for this package,
    ?DirichletMultinomial."""

    bioc = "DirichletMultinomial"

    version("1.42.0", commit="c388536bed4bdc57724b704edec04b28acbf48db")
    version("1.40.0", commit="200176f8c72ff127788c500629b71872bc6b1f83")
    version("1.38.0", commit="b4de83d354e974fdb7cb3526d029487f24aab670")
    version("1.36.0", commit="926baff6c75cb498945c5895f25cc143c907a357")
    version("1.32.0", commit="6949abab2462b2c09f7a0ca5b5cbf0c95a40ad16")
    version("1.26.0", commit="7daa84948020811bb8a27d2e633fccfdcdd1018f")
    version("1.24.1", commit="50195d9b1986852da29100e77f6f09df5d6e2a35")
    version("1.22.0", commit="5864f4298105d12f345f27df77ad13bae4061ca5")
    version("1.20.0", commit="251529f301da1482551142240aeb6baf8dab2272")
    version("1.18.0", commit="81ccc8d83b8ef84f5d3e877bc0a04233a0f63c51")

    depends_on("c", type="build")  # generated

    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("gsl")
