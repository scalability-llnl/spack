# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHighr(RPackage):
    """Syntax Highlighting for R Source Code.

    Provides syntax highlighting for R source code. Currently it supports
    LaTeX and HTML output. Source code of other languages is supported via
    Andre Simon's highlight package."""

    cran = "highr"

    license("GPL-2.0-or-later")

    version("0.11", sha256="e90d14284001963325a84a9dbeef029609d52515da8d65c87ae61be21b7fe0a7")
    version("0.10", sha256="ec55bc1ff66390ed66806dc2a7b6c17dbfd089b3d73fe2e369017f8cb4bc347b")
    version("0.9", sha256="beff11390d936c90fdcc00e7ed0eb72220f3de403a51b56659e3d3e0b6d8ed4d")
    version("0.8", sha256="4bd01fba995f68c947a99bdf9aca15327a5320151e10bd0326fad50a6d8bc657")
    version("0.7", sha256="cabba5b6f2ea82024a49c5ced5f1aa476f864bc52bc129038e319e4e26b6f3b7")
    version("0.6", sha256="43e152b2dea596df6e14c44398c74fcd438ece15eaae5bdb84aef8d61b213b59")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.2.3:", type=("build", "run"), when="@0.8:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.10:")
    depends_on("r-xfun@0.18:", type=("build", "run"), when="@0.9:")
