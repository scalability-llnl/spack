# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagrittr(RPackage):
    """A Forward-Pipe Operator for R.

    Provides a mechanism for chaining commands with a new forward-pipe
    operator, %>%. This operator will forward a value, or the result of an
    expression, into the next function call/expression. There is flexible
    support for the type of right-hand side expressions. For more information,
    see package vignette."""

    cran = "magrittr"

    license("MIT")

    version("2.0.3", sha256="a2bff83f792a1acb801bfe6330bb62724c74d5308832f2cb6a6178336ace55d2")
    version("2.0.2", sha256="7be6fd0d0da75b92d8bad0136076da96260ee84bf639ef632a24668acdc163a6")
    version("2.0.1", sha256="75c265d51cc2b34beb27040edb09823c7b954d3990a7a931e40690b75d4aad5f")
    version("1.5", sha256="05c45943ada9443134caa0ab24db4a962b629f00b755ccf039a2a2a7b2c92ae8")

    depends_on("c", type="build")  # generated

    depends_on("r@3.4.0:", type=("build", "run"), when="@2.0.3:")
