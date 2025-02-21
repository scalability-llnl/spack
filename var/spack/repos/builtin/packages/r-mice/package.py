# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMice(RPackage):
    """Multivariate Imputation by Chained Equations.

    Multiple imputation using Fully Conditional Specification (FCS) implemented
    by the MICE algorithm as described in Van Buuren and Groothuis-Oudshoorn
    (2011) <doi:10.18637/jss.v045.i03>.  Each variable has its own imputation
    model. Built-in imputation models are provided for continuous data
    (predictive mean matching, normal), binary data (logistic regression),
    unordered categorical data (polytomous logistic regression) and ordered
    categorical data (proportional odds). MICE can also impute continuous
    two-level data (normal model, pan, second-level variables). Passive
    imputation can be used to maintain consistency between variables. Various
    diagnostic plots are available to inspect the quality of the
    imputations."""

    cran = "mice"

    license("GPL-2.0-or-later")

    version("3.16.0", sha256="29f0285185a540337e9dde2357690c82d174f115be701ee2f0a7083173a44040")
    version("3.15.0", sha256="3d64dd260e3dce9c4c2f7be8c99f3063769df9ccfd3a0fc827c2de0ac842e87b")
    version("3.14.0", sha256="f87bb73d8bfee36c6bf4f15779c59ff6b70c70ca25b1388b4ee236757276d605")
    version("3.12.0", sha256="575d9e650d5fc8cd66c0b5a2f1e659605052b26d61f772fff5eed81b414ef144")
    version("3.6.0", sha256="7bc72bdb631bc9f67d8f76ffb48a7bb275228d861075e20c24c09c736bebec5d")
    version("3.5.0", sha256="4fccecdf9e8d8f9f63558597bfbbf054a873b2d0b0820ceefa7b6911066b9e45")
    version("3.0.0", sha256="98b6bb1c5f8fb099bd0024779da8c865146edb25219cc0c9542a8254152c0add")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-broom", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-generics", type=("build", "run"), when="@3.12.0:")
    depends_on("r-glmnet", type=("build", "run"), when="@3.16.0:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mitml", type=("build", "run"), when="@3.16.0:")
    depends_on("r-nnet", type=("build", "run"), when="@3.16.0:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"), when="@3.16.0:")
    depends_on("r-tidyr", type=("build", "run"), when="@3.12.0:")
    depends_on("r-cpp11", type=("build", "run"), when="@3.12.0:")

    depends_on("r-mitml", type=("build", "run"), when="@:3.6.0")
    depends_on("r-nnet", type=("build", "run"), when="@:3.6.0")
    depends_on("r-rpart", type=("build", "run"), when="@:3.6.0")
    depends_on("r-survival", type=("build", "run"), when="@:3.6.0")
    depends_on("r-mass", type=("build", "run"), when="@:3.6.0")
    depends_on("r-withr", type=("build", "run"), when="@3.14.0:3.14.0")
