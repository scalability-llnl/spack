# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProfvis(RPackage):
    """Interactive visualizations for profiling R code."""

    cran = "profvis"

    license("GPL-3.0-only OR custom")

    version("0.3.8", sha256="ec02c75bc9907a73564e691adfa8e06651ca0bd73b7915412960231cd265b4b2")
    version("0.3.7", sha256="43974863cb793f81dbea4b94096343c321f7739c9038980405c9b16b04a906b9")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-htmlwidgets@0.3.2:", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"), when="@0.3.8:")
    depends_on("r-rlang@0.4.9:", type=("build", "run"), when="@0.3.8:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"), when="@0.3.8:")
