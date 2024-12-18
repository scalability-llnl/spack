# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REllipsis(RPackage):
    """Tools for Working with ...

    The ellipsis is a powerful tool for extending functions. Unfortunately
    this power comes at a cost: misspelled arguments will be silently ignored.
    The ellipsis package provides a collection of functions to catch problems
    and alert the user."""

    cran = "ellipsis"

    license("MIT")

    version("0.3.2", sha256="a90266e5eb59c7f419774d5c6d6bd5e09701a26c9218c5933c9bce6765aa1558")
    version("0.3.1", sha256="4f8a15158dfc27cdc0f7554c7a61e92b02e4d70bfc3d968f01a99da2189b75db")
    version("0.3.0", sha256="0bf814cb7a1f0ee1f2949bdc98752a0d535f2a9489280dd4d8fcdb10067ee907")
    version("0.2.0.1", sha256="0e6528c5e8016c3617cc1cfcdb5a4bfeb073e0bd5ea76b43e56b0c3208a0a943")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@0.3:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"))
