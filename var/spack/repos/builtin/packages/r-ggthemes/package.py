# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgthemes(RPackage):
    """Extra Themes, Scales and Geoms for 'ggplot2'.

    Some extra themes, geoms, and scales for 'ggplot2'. Provides 'ggplot2'
    themes and scales that replicate the look of plots by Edward Tufte, Stephen
    Few, 'Fivethirtyeight', 'The Economist', 'Stata', 'Excel', and 'The Wall
    Street Journal', among others. Provides 'geoms' for Tufte's box plot and
    range frame."""

    cran = "ggthemes"

    license("GPL-2.0-only")

    version("5.1.0", sha256="074819acfe8bb2233426a0fef3bb448c5ce817bb14d517252fa05932e28bbd0e")
    version("4.2.4", sha256="7b35168cf5b68f6f52dd533a1b345ec87e09d1a85ca68e8dc5377cdf95718567")
    version("4.2.0", sha256="5bb3fe94819fe2cce7865f07a6e6ea5c59d3996f78d1c0836ad406f69efb3367")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@5.0.0:")
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
