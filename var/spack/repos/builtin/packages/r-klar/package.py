# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKlar(RPackage):
    """Classification and Visualization.

    Miscellaneous functions for classification and visualization, e.g.
    regularized discriminant analysis, sknn() kernel-density naive Bayes, an
    interface to 'svmlight' and stepclass() wrapper variable selection for
    supervised classification, partimat() visualization of classification rules
    and shardsplot() of cluster results as well as kmodes() clustering for
    categorical data, corclust() variable clustering, variable extraction from
    different variable clustering models and weight of evidence
    preprocessing."""

    cran = "klaR"

    version("1.7-3", sha256="d36c041c017cdb5ba3dbf7fb61d5ce3908d8e780eb2912fc99471394fcb8e3e5")
    version("1.7-2", sha256="8035c3edb8257973184ad5a2109fc7c77c32da913cb9dd0c2f1c373e6fccbd61")
    version("1.7-1", sha256="0354bafb1a202bc439660ecfcfe78359bc2881a69d15ff64afa049e4eb171d25")
    version("1.7-0", sha256="b4795250ef19fd1b5e1b9a59343fd01159a33dbdbb504a06258220e37a718198")
    version("0.6-15", sha256="5bfe5bc643f8a64b222317732c26e9f93be297cdc318a869f15cc9ab0d9e0fae")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-combinat", type=("build", "run"))
    depends_on("r-questionr", type=("build", "run"))

    # NOTE: The svmlight interface is not built. The external svmlight package
    # dates back to 2008, and does not build with modern compilers. In
    # addition, the tarfile is unversioned and its distribution is restricted.
