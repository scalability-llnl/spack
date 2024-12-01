# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShinyjs(RPackage):
    """Easily Improve the User Experience of Your Shiny Apps in Seconds.

    Perform common useful JavaScript operations in Shiny apps that will greatly
    improve your apps without having to know any JavaScript. Examples include:
    hiding an element, disabling an input, resetting an input back to its
    original value, delaying code execution by a few seconds, and many more
    useful functions for both the end user and the developer. 'shinyjs' can
    also be used to easily call your own custom JavaScript functions from R."""

    cran = "shinyjs"

    license("MIT")

    version("2.1.0", sha256="7ec20cbf1b1fd7a32d85a56dfc0df8b5f67c828d241da400a21d893cb37ea9c5")
    version("2.0.0", sha256="c2cdd9fab41f6b46bb41b288cd9b3fb3a7fe9627b664e3a58a0cb5dd4c19f8ff")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-digest@0.6.8:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-shiny@1.0.0:", type=("build", "run"))

    depends_on("r-htmltools@0.2.9:", type=("build", "run"), when="@:2.0.0")
    depends_on("pandoc", type="build", when="@:2.0.0")
