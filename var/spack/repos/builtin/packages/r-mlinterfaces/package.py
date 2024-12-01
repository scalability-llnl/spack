# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMlinterfaces(RPackage):
    """Uniform interfaces to R machine learning procedures for data in
    Bioconductor containers.

    This package provides uniform interfaces to machine learning code for
    data in R and Bioconductor containers."""

    bioc = "MLInterfaces"

    version("1.80.0", commit="275f8d39f05c46ab3ab7096d1e0539a33bab3a54")
    version("1.78.0", commit="0988b95d282a6bffe56b7df4da2e23485e96d12c")
    version("1.76.0", commit="935323d8ce1e4bbf41844a1f9b6c946c5a30c673")
    version("1.74.0", commit="5ee73b6491b1d68d7b49ddce6483df98ad880946")
    version("1.70.0", commit="7b076c3e85314dd5fd5bd8a98e8123d08d9acd3b")
    version("1.64.1", commit="0b081112d87771248bc33b3b82d5ca4685f986a1")
    version("1.62.1", commit="6cf59a90b14779cf57a0b36f1087304082ae50fe")
    version("1.60.1", commit="019e9ed44923e5d845a4800246aa044ddd59d548")
    version("1.58.1", commit="4e2b5efa019fcb677dc82a58a1668c8a00cdfe07")
    version("1.56.0", commit="31fe6fb20d859fcb01d5552f42bca6bab16cc67f")

    depends_on("r@2.9:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.60.1:")
    depends_on("r-rcpp", type=("build", "run"), when="@1.70.0:")
    depends_on("r-biocgenerics@0.13.11:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-gdata", type=("build", "run"))
    depends_on("r-pls", type=("build", "run"))
    depends_on("r-sfsmisc", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-fpc", type=("build", "run"))
    depends_on("r-ggvis", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"))
    depends_on("r-gbm", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-hwriter", type=("build", "run"))
    depends_on("r-threejs@0.2.2:", type=("build", "run"))
    depends_on("r-mlbench", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"), when="@1.74.0:")
    depends_on("r-summarizedexperiment", type=("build", "run"), when="@1.78.0:")

    depends_on("r-rda", type=("build", "run"), when="@:1.64.1")
