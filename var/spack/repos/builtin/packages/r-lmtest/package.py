# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLmtest(RPackage):
    """Testing Linear Regression Models.

    A collection of tests, data sets, and examples for diagnostic checking in
    linear regression models. Furthermore, some generic tools for inference in
    parametric models are provided."""

    cran = "lmtest"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("0.9-40", sha256="64400d4d6cc635316531042971f1783539686e9015c76f5741c07304fa14d997")
    version("0.9-39", sha256="71f8d67cbe559b33fe02910a3e98cddc60c9dcc421c64f7878c647218f07d488")
    version("0.9-38", sha256="32a22cea45398ffc5732d9f5c0391431d0cdd3a9e29cc7b77bea32c1eb4a216b")
    version("0.9-37", sha256="ddc929f94bf055974832fa4a20fdd0c1eb3a84ee11f716c287936f2141d5ca0a")
    version("0.9-36", sha256="be9f168d6554e9cd2be0f9d8fc3244f055dce90d1fca00f05bcbd01daa4ed56b")
    version("0.9-34", sha256="86eead67ed6d6c6be3fbee97d5ce45e6ca06a981f974ce01a7754a9e33770d2e")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
