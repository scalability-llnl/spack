# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIpred(RPackage):
    """Improved Predictors.

    Improved predictive models by indirect classification and bagging for
    classification, regression and survival problems  as well as resampling
    based estimators of prediction error."""

    cran = "ipred"

    license("GPL-2.0-or-later")

    version("0.9-15", sha256="a4752de11121262f3f4c43163efa34e05e42cdf4f8496d8897be6f410dc0ee4b")
    version("0.9-14", sha256="81c83dc847d09c3db52ef15e36cd4dac38c50eead1008ddd458b9e89d7528f35")
    version("0.9-13", sha256="6168a062d93c2d3063c064a8f242cd3716dee99822e20363a1801261319c4c98")
    version("0.9-12", sha256="d6e1535704d39415a799d7643141ffa4f6f55597f03e763f4ccd5d8106005843")
    version("0.9-9", sha256="0da87a70730d5a60b97e46b2421088765e7d6a7cc2695757eba0f9d31d86416f")
    version("0.9-8", sha256="9c1d11c3cb0d72be7870e70a216e589e403bbfee38c796fe75cd0611d878ac07")
    version("0.9-5", sha256="3a466417808e17c4c6cd0f2b577407355d9da79a341558b42a8b76e24b6f6ba4")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-rpart@3.1-8:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-class", type=("build", "run"))
    depends_on("r-prodlim", type=("build", "run"))
