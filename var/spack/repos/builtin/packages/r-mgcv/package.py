# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMgcv(RPackage):
    """Mixed GAM Computation Vehicle with Automatic Smoothness Estimation.

    Generalized additive (mixed) models, some of their extensions and  other
    generalized ridge regression with multiple smoothing  parameter estimation
    by (Restricted) Marginal Likelihood,  Generalized Cross Validation and
    similar, or using iterated  nested Laplace approximation for fully Bayesian
    inference. See  Wood (2017) <doi:10.1201/9781315370279> for an overview.
    Includes a gam() function, a wide variety of smoothers, 'JAGS'  support and
    distributions beyond the exponential family."""

    cran = "mgcv"

    license("GPL-2.0-or-later")

    version("1.9-1", sha256="700fbc37bedd3a49505b9bc4949faee156d9cfb4f669d797d06a10a15a5bdb32")
    version("1.8-42", sha256="087fc38b64ad06f2149eafc54f2679dd8840cf6fc488e66cf131e3c1de2db6c7")
    version("1.8-41", sha256="2f7a030fe2be75edef6bd96147df46c2262f3cdc44c383d8f82b401df44fe690")
    version("1.8-40", sha256="dbe627266c3b339232e2d4228d5370ba88c86540319e6891d161242efba7e4a5")
    version("1.8-38", sha256="cd12ed5787d6fdcead34e782e48b62b3f9efd523616c906e2da77bd9c142ddbb")
    version("1.8-33", sha256="98cb7bac928e2c9564091a9af31e5d309305c6c5fcf96e8429c08925fe6f2bf4")
    version("1.8-28", sha256="b55ea8227cd5c263c266c3885fa3299aa6bd23b54186517f9299bf38a7bdd3ea")
    version("1.8-27", sha256="c88b99fb518decd7e9cd17a4c267e74f98a78172f056784194b5b127ca0f7d1b")
    version("1.8-22", sha256="d4af7767e097ebde91c61d5ab4c62975dcb6b4ed6f545c09f5276a44ebc585cf")
    version("1.8-21", sha256="b1826e40af816226d230f5b7dad6e7646cfefe840036e50c6433e90a23f9f2ed")
    version("1.8-20", sha256="6540358c6f11341c997f8712a6edb590c8af0b1546e14e92724021a8d49f1375")
    version("1.8-19", sha256="b9a43281fc25fb96de94cf2a7ca48aafa1ca895b279d980398bc3a4f3074996c")
    version("1.8-18", sha256="29ae8ebc76f40cc5cfa775ffece99aea437d9f2f48482c48bd4b31727175df6a")
    version("1.8-17", sha256="8ff3eb28c83ba7c9003005e7fe08028627fb673b9b07c0462b410e45e81042fe")
    version("1.8-16", sha256="9266a0cbd783717fc6130db4e0034e69465d177397687f35daf6a8ccdb0b435e")
    version("1.8-13", sha256="74bc819708ef59da94b777a446ef00d7f14b428eec843533e824017c29cc524b")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.8.34:")
    depends_on("r-nlme@3.1-64:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
