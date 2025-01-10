# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSandwich(RPackage):
    """Robust Covariance Matrix Estimators.

    Object-oriented software for model-robust covariance matrix estimators.
    Starting out from the basic  robust Eicker-Huber-White sandwich covariance
    methods include: heteroscedasticity-consistent (HC) covariances for
    cross-section data; heteroscedasticity- and autocorrelation-consistent
    (HAC) covariances for time series data (such as Andrews' kernel HAC,
    Newey-West, and WEAVE estimators); clustered covariances (one-way and
    multi-way); panel and panel-corrected covariances;
    outer-product-of-gradients covariances; and (clustered) bootstrap
    covariances. All methods are applicable to (generalized) linear model
    objects fitted by lm() and glm() but can also be adapted to other classes
    through S3 methods. Details can be found in Zeileis et al. (2020)
    <doi:10.18637/jss.v095.i01>, Zeileis (2004) <doi:10.18637/jss.v011.i10> and
    Zeileis (2006) <doi:10.18637/jss.v016.i09>."""

    cran = "sandwich"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("3.1-0", sha256="96b0e105ee50391a1fd286e9556ba6669f08565fa30788b1a21bc861b0a023fa")
    version("3.0-2", sha256="6e30b6b554eb19430a60c45a8132fb7918ddb0013577bf6a62caeb163bdfe2b4")
    version("3.0-1", sha256="f6584b7084f3223bbc0c4722f53280496be73849747819b0cb4e8f3910284a89")
    version("3.0-0", sha256="828fe53b5e09db5015efd529b2db4dcd40251bce110fea7b0b219fa9ac36d529")
    version("2.5-1", sha256="dbef6f4d12b83e166f9a2508b7c732b04493641685d6758d29f3609e564166d6")
    version("2.5-0", sha256="6cc144af20739eb23e5539010d3833d7c7fc53cbca2addb583ab933167c11399")
    version("2.3-4", sha256="2052f7e3d19a05c372f422c5480f1058a4107e420cd038a9bd7240c4f0746d4d")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"), when="@3.0-0:")
    depends_on("r-zoo", type=("build", "run"))
