# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppziggurat(RPackage):
    """'Rcpp' Integration of Different "Ziggurat" Normal RNG Implementations.

    The Ziggurat generator for normally distributed random numbers, originally
    proposed by Marsaglia and Tsang (2000, <doi:10.18637/jss.v005.i08>) has
    been improved upon a few times starting with Leong et al (2005,
    <doi:10.18637/jss.v012.i07>). This package provides an aggregation in order
    to compare different implementations in order to provide an 'faster but
    good enough' alternative for use with R and C++ code."""

    cran = "RcppZiggurat"

    version("0.1.6", sha256="9c78255ca476c945c05a564d1e4da363de714d890e0e27f3b252fd73c50eed71")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"), when="@0.1.6:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcppgsl", type=("build", "run"))

    # not listed as a dependency but needed
    depends_on("gsl")
