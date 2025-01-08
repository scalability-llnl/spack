# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDoby(RPackage):
    """Groupwise Statistics, LSmeans, Linear Estimates, Utilities.

    Utility package containing: 1) Facilities for working with grouped data:
        'do' something to data stratified 'by' some variables. 2) LSmeans
        (least-squares means), general linear estimates. 3) Restrict functions
        to a smaller domain. 4) Miscellaneous other utilities."""

    cran = "doBy"

    version("4.6.22", sha256="2aa7e236de98af73de54a46214ceac50fdf69d90b12bb37f2779a501f40b0b0d")
    version("4.6.16", sha256="d5937eb57d293b0bc2e581ff2e1e628671cb4eacddc0b9574dc28a5316ecbbe7")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@4.6.18:")
    depends_on("r@4.2.0:", type=("build", "run"), when="@4.6.21:")
    depends_on("r-boot", type=("build", "run"), when="@4.6.21:")
    depends_on("r-broom", type=("build", "run"))
    depends_on("r-cowplot", type=("build", "run"), when="@4.6.21:")
    depends_on("r-deriv", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-microbenchmark", type=("build", "run"))
    depends_on("r-modelr", type=("build", "run"), when="@4.6.21:")
    depends_on("r-rlang", type=("build", "run"), when="@4.6.21:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"), when="@4.6.21:")

    depends_on("r-magrittr", type=("build", "run"), when="@:4.6.20")
    depends_on("r-pbkrtest@0.4-8.1:", type=("build", "run"), when="@:4.6.21")
