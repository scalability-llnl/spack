# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChemometrics(RPackage):
    """Multivariate Statistical Analysis in Chemometrics.

    R companion to the book "Introduction to Multivariate Statistical Analysis
    in Chemometrics" written by K. Varmuza and P. Filzmoser (2009)."""

    cran = "chemometrics"

    license("GPL-3.0-or-later")

    version("1.4.4", sha256="fd0edb1ebe321ff7677d0a668d7dfc79a7cd55f408a53d1f13db4cf6347aa881")
    version("1.4.2", sha256="b705832fa167dc24b52b642f571ed1efd24c5f53ba60d02c7797986481b6186a")
    version("1.4.1", sha256="7646da0077657d672356204aa2094be68e10ec13617f92ae97ff53a389053905")
    version("1.3.9", sha256="553eda53789b6a4d0f77842c175f98be5b9a04bccc9d2ba0ecde1bb5c8a53f21")
    version("1.3.8", sha256="5a977bf1a9475d4dd4764ec9e99cbce237c5b624ef9aa96fcaf08406b1b8a56d")
    version("1.3.7", sha256="653a4f728c996983a4b5e5144229d0cf8b6754fb7e85e9014eeaf34fa19da42f")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-mclust", type=("build", "run"))
    depends_on("r-lars", type=("build", "run"))
    depends_on("r-robustbase", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-pls", type=("build", "run"))
    depends_on("r-som", type=("build", "run"))
    depends_on("r-pcapp", type=("build", "run"))
    depends_on("r-class", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
