# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhilentropy(RPackage):
    """Similarity and Distance Quantification Between Probability Functions.

    Computes 46 optimized distance and similarity measures for comparing
    probability functions (Drost (2018) <doi:10.21105/joss.00765>). These
    comparisons between probability functions have their foundations in a broad
    range of scientific disciplines from mathematics to ecology. The aim of
    this package is to provide a core framework for clustering, classification,
    statistical inference, goodness-of-fit, non-parametric statistics,
    information theory, and machine learning tasks that are based on comparing
    univariate or multivariate probability functions."""

    cran = "philentropy"

    license("GPL-2.0-only")

    version("0.8.0", sha256="3aa6d4918168f4fe2c56ea3f26381b0ffc02f1d5b9b95e294bac1a34bf66be3e")
    version("0.7.0", sha256="ce72e2327aee80aeeb630caa33be6a35e4f2b8a7491842d8c21099b9c43584b7")
    version("0.6.0", sha256="138acf2aedab17c9d367def378e35c8aba80d9e786284b2866955cea1c24eeb6")
    version("0.5.0", sha256="b39e9a825458f3377e23b2a133180566780e89019e9d22a6a5b7ca87c49c412f")
    version("0.4.0", sha256="bfd30bf5635aab6a82716299a87d44cf96c7ab7f4ee069843869bcc85c357127")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
    depends_on("r-poorman", type=("build", "run"), when="@0.6.0:")

    depends_on("r-dplyr", type=("build", "run"), when="@:0.5.0")
