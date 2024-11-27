# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCar(RPackage):
    """Companion to Applied Regression.

    Functions and Datasets to Accompany J. Fox and S. Weisberg, An R Companion
    to Applied Regression, Second Edition, Sage, 2011."""

    cran = "car"

    license("GPL-2.0-or-later")

    version("3.1-2", sha256="89263491977ac8e9406b2f4b1638bf06c7ddd1b0e0e3ecda4be61420474674c8")
    version("3.1-1", sha256="8fc55815eed7e46a32b54da9e0bfa4b74a8d082d73d896e3372f2a413b6bd2bc")
    version("3.1-0", sha256="bd52b4eaea46ce828fccd93445301d06ebd265e2ffff796064875a8c0f0aea21")
    version("3.0-13", sha256="d35ae8da80284c9e4471ff13e7100c3cdc1809fd06f813cd223a3958e29e47eb")
    version("3.0-12", sha256="b899a6efae3842a90a2349d381dbcf4b4ed36bd03108ebe7380e81120e457302")
    version("3.0-11", sha256="b32c927206f515631ff276dbb337b0f22e9b2d851f4abb1d2c272e534c19542c")
    version("3.0-10", sha256="1ce316d2fee9b47c951d25d096be732489a3c9f6fc9e612a1eca2e50fb5925f1")
    version("3.0-3", sha256="fa807cb12f6e7fb38ec534cac4eef54747945c2119a7d51155a2492ad778c36f")
    version("3.0-2", sha256="df59a9ba8fed67eef5ddb8f92f2b41745df715d5695c71d562d7031513f37c50")
    version("2.1-4", sha256="fd39cf1750cb560a66623fea3fa9e6a94fc24e3dc36367aff24df7d0743edb28")
    version("2.1-2", sha256="8cc3e57f172c8782a08960b508906d3201596a21f4b6c1dab8d4e59353093652")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.0-3:")
    depends_on("r-cardata@3.0-0:", type=("build", "run"), when="@3.0:")
    depends_on("r-abind", type=("build", "run"), when="@3.0:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-pbkrtest@0.4-4:", type=("build", "run"))
    depends_on("r-quantreg", type=("build", "run"))
    depends_on("r-rio", type=("build", "run"), when="@3.0:3.0-11")
    depends_on("r-lme4", type=("build", "run"), when="@3.0:")
    depends_on("r-lme4@1.1-27.1:", type=("build", "run"), when="@3.0-11:")
    depends_on("r-nlme", type=("build", "run"), when="@3.0:")
    depends_on("r-scales", type=("build", "run"), when="@3.1-1:")
    depends_on("r-maptools", type=("build", "run"), when="@3.0:3.1-0")
