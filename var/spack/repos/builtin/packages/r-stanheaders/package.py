# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStanheaders(RPackage):
    """C++ Header Files for Stan.

    The C++ header files of the Stan project are provided by this package, but
    it contains no R code, vignettes, or function documentation. There is a
    shared object containing part of the CVODES library, but it is not
    accessible from R. StanHeaders is only useful for developers who want to
    utilize the LinkingTo directive of their package's DESCRIPTION file to
    build on the Stan library without incurring unnecessary dependencies. The
    Stan project develops a probabilistic programming language that implements
    full or approximate Bayesian statistical inference via Markov Chain Monte
    Carlo or variational methods and implements (optionally penalized) maximum
    likelihood estimation via optimization. The Stan library includes an
    advanced automatic differentiation scheme, templated statistical and linear
    algebra functions that can handle the automatically differentiable scalar
    types (and doubles, ints, etc.), and a parser for the Stan language. The
    'rstan' package provides user-facing R functions to parse, compile, test,
    estimate, and analyze Stan models."""

    cran = "StanHeaders"

    version("2.32.10", sha256="c3125b8d7dc4c6b7082258b2fa6c9530c2e4714c89ffd08b8e72f4c9f4108582")
    version("2.21.0-7", sha256="27546e064f0e907e031d9185ad55245d118d82fbe3074ecb1d76fae8b9f2336b")
    version("2.21.0-6", sha256="a0282a054d0e6ab310ec7edcffa953b77c7e4a858d9ac7028aab1b4fb4ce8cf3")
    version("2.18.1-10", sha256="8a9f7e22105428e97d14f44f75395c37cf8c809de148d279c620024452b3565a")
    version("2.18.1", sha256="ce0d609a7cd11725b1203bdeae92acc54da3a48b8266eb9dbdb9d95b14df9209")
    version("2.17.1", sha256="4300a1910a2eb40d7a6ecabea3c1e26f0aa9421eeb3000689272a0f62cb80d97")
    version("2.10.0-2", sha256="ce4e335172bc65da874699302f6ba5466cdbcf69458c11954c0f131fc78b59b7")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@2.18.0:")
    depends_on("r-rcppparallel@5.0.1:", type=("build", "run"), when="@2.21.0:")
    depends_on("r-rcppparallel@5.1.4:", type=("build", "run"), when="@2.26.25:")
    depends_on("r-rcppeigen", type=("build", "run"), when="@2.21.0:")
    depends_on("r-rcppeigen@0.3.4.0.0:", type=("build", "run"), when="@2.32.8:")
    depends_on("pandoc", type="build")
