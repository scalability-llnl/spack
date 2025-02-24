# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgstats(RPackage):
    """Provides new statistics, new geometries and new positions for
    'ggplot2' and a suite of functions to facilitate the creation of
    statistical plots."""

    homepage = "https://larmarange.github.io/ggstats/"
    cran = "ggstats"

    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("0.6.0", sha256="f80aaa229f542cb18174b9ab82b0026c6bd3331f22bf2662712ab6af480b6d80")

    depends_on("r-broom-helpers@1.14.0:", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-forcats", type=("build", "run"))
    depends_on("r-ggplot2@3.4.0:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-patchwork", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
