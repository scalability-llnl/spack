# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGbm(RPackage):
    """Generalized Boosted Regression Models.

    An implementation of extensions to Freund and Schapire's AdaBoost algorithm
    and Friedman's gradient boosting machine. Includes regression methods for
    least squares, absolute loss, t-distribution loss, quantile regression,
    logistic, multinomial logistic, Poisson, Cox proportional hazards  partial
    likelihood, AdaBoost exponential loss, Huberized hinge loss, and  Learning
    to Rank measures (LambdaMart). Originally developed by Greg Ridgeway."""

    cran = "gbm"

    license("GPL-2.0-or-later OR custom")

    version("2.2.2", sha256="029ad2bac10c98979cf69206e94f2cc51a50667ec035f2474c44fb841950c4f4")
    version("2.1.8.1", sha256="8d2456124552658ee9500707c4e9992cf42cb88705008c32ea258efb4f2be80b")
    version("2.1.8", sha256="7d5de3b980b8f23275e86ac9bed48a497c9aa53c58e407dfd676309f38272ec1")
    version("2.1.5", sha256="06fbde10639dfa886554379b40a7402d1f1236a9152eca517e97738895a4466f")
    version("2.1.3", sha256="eaf24be931d762f1ccca4f90e15997719d01005f152160a3d20d858a0bbed92b")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))

    depends_on("r-gridextra", type=("build", "run"), when="@2.1.5")
