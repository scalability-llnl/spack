# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUwot(RPackage):
    """The Uniform Manifold Approximation and Projection (UMAP) Method for
    Dimensionality Reduction.

    An implementation of the Uniform Manifold Approximation and Projection
    dimensionality reduction by McInnes et al. (2018) <arXiv:1802.03426>. It
    also provides means to transform new data and to carry out supervised
    dimensionality reduction. An implementation of the related LargeVis method
    of Tang et al. (2016) <arXiv:1602.00370> is also provided. This is a
    complete re-implementation in R (and C++, via the 'Rcpp' package): no
    Python installation is required. See the uwot website
    (<https://github.com/jlmelville/uwot>) for more documentation and
    examples."""

    cran = "uwot"

    license("GPL-3.0-or-later")

    version("0.2.2", sha256="d9938c43d29530d4b36d1b2649cc679b09945a740db2cd3a266242b1aa9a6cd1")
    version("0.1.14", sha256="8016e8192b7e72604ca71840cbe43fa1d2caed8a8ad7cbf20e85cd3b384a9fe0")
    version("0.1.11", sha256="4fcf90f1369a2a1f01db9e05a2365b155b2ada8e51e1f7f3ba5122d86affd41b")
    version("0.1.10", sha256="6ee1b6027bce679cd5a35f647f516a5b327632234bcf323c7f3d5b5e10807d23")
    version("0.1.3", sha256="4936e6922444cae8a71735e945b6bb0828a1012232eb94568054f78451c406d7")

    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-fnn", type=("build", "run"))
    depends_on("r-rcppannoy@0.0.11:", type=("build", "run"))
    depends_on("r-rcppannoy@0.0.17:", type=("build", "run"), when="@0.1.10:")
    depends_on("r-irlba", type=("build", "run"))
    depends_on("r-rcppprogress", type=("build", "run"))
    depends_on("r-rspectra", type=("build", "run"), when="@0.2.2:")
    depends_on("r-dqrng", type=("build", "run"))

    depends_on("r-rcppparallel", type=("build", "run"), when="@:0.1.3")
    depends_on("gmake", type="build", when="@:0.1.3")
    depends_on("r-rspectra", type=("build", "run"), when="@:0.1.11")
