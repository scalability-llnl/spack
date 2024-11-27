# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFutileLogger(RPackage):
    """A Logging Utility for R.

    Provides a simple yet powerful logging utility. Based loosely on log4j,
    futile.logger takes advantage of R idioms to make logging a convenient and
    easy to use replacement for cat and print statements."""

    cran = "futile.logger"

    version("1.4.3", sha256="5e8b32d65f77a86d17d90fd8690fc085aa0612df8018e4d6d6c1a60fa65776e4")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-lambda-r@1.1.0:", type=("build", "run"))
    depends_on("r-futile-options", type=("build", "run"))
