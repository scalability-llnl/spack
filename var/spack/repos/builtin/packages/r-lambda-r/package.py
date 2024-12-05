# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLambdaR(RPackage):
    """Modeling Data with Functional Programming.

    A language extension to efficiently write functional programs in R.  Syntax
    extensions include multi-part function definitions, pattern matching, guard
    statements, built-in (optional) type safety."""

    cran = "lambda.r"

    version("1.2.4", sha256="d252fee39065326c6d9f45ad798076522cec05e73b8905c1b30f95a61f7801d6")
    version("1.2.3", sha256="0cd8e37ba1a0960888016a85d492da51a57df54bd65ff920b08c79a3bfbe8631")
    version("1.2", sha256="7dc4188ce1d4a6b026a1b128719ff60234ae1e3ffa583941bbcd8473ad18146f")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-formatr", type=("build", "run"))
