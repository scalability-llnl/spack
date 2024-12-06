# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocneighbors(RPackage):
    """Nearest Neighbor Detection for Bioconductor Packages.

    Implements exact and approximate methods for nearest neighbor detection,
    in a framework that allows them to be easily switched within
    Bioconductor packages or workflows. Exact searches can be performed
    using the k-means for k-nearest neighbors algorithm or with vantage
    point trees. Approximate searches can be performed using the Annoy or
    HNSW libraries. Searching on either Euclidean or Manhattan distances is
    supported. Parallelization is achieved for all methods by using
    BiocParallel. Functions are also provided to search for all neighbors
    within a given distance."""

    bioc = "BiocNeighbors"

    version("1.18.0", commit="4b19ef2a76baa0b001c426bad540ab9295bec78e")
    version("1.16.0", commit="3b227beead424314aab5ef847222f8f4243c684f")
    version("1.14.0", commit="670a1bd4d82636d28fbff50cea2157e16bb1a858")
    version("1.12.0", commit="3c8a290f75adc944b408e6e77a36f3a0c1509c4c")
    version("1.8.2", commit="889bc91f8cb45d210b47ae5c0b9cfb86fb071ca2")
    version("1.2.0", commit="f754c6300f835142536a4594ddf750481e0fe273")
    version("1.0.0", commit="e252fc04b6d22097f2c5f74406e77d85e7060770")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.5:", type=("build", "run"), when="@1.0.0")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"), when="@1.8.2:")
    depends_on("r-rcpphnsw", type=("build", "run"), when="@1.2.0:")

    depends_on("r-rcppannoy", type=("build", "run"), when="@:1.2.0")
    depends_on("r-biocgenerics", type=("build", "run"), when="@1.2.0")
