# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RServr(RPackage):
    """A Simple HTTP Server to Serve Static Files or Dynamic Documents.

    Start an HTTP server in R to serve static files, or dynamic documents that
    can be converted to HTML files (e.g., R Markdown) under a given
    directory."""

    cran = "servr"

    license("GPL-2.0-or-later")

    version("0.30", sha256="43f920161408871a042462b7c3353149a608941253541a19a9ce3408f9882d40")
    version("0.26", sha256="7588d7e00d5b2f77b0737f164f3d7b0ba7b1e8b60c0372a1d6452096e2d2031c")
    version("0.25", sha256="e6ae0d4c09e9037268b1c291c36c93ba0a74c31fe2fcb1f0652b2ae9fca5e73c")
    version("0.24", sha256="d94e1d31802ce6bbab7a5838ff94cbca8cd998237d834ff25fedf7514f41a087")
    version("0.21", sha256="3fc0da063dd04b796a49ce62bf8e69d5854679520da90cc92ee3fc0a0b2ad389")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-mime@0.2:", type=("build", "run"))
    depends_on("r-httpuv@1.5.2:", type=("build", "run"))
    depends_on("r-xfun", type=("build", "run"))
    depends_on("r-xfun@0.42:", type=("build", "run"), when="@0.29:")
    depends_on("r-jsonlite", type=("build", "run"))
