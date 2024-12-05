# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJanitor(RPackage):
    """Simple Tools for Examining and Cleaning Dirty Data.

    The main janitor functions can: perfectly format data.frame column names;
    provide quick one- and two-variable tabulations (i.e., frequency tables and
    crosstabs); and isolate duplicate records. Other janitor functions nicely
    format the tabulation results. These tabulate-and-report functions
    approximate popular features of SPSS and Microsoft Excel. This package
    follows the principles of the "tidyverse" and works well with the pipe
    function %>%. janitor was built with beginning-to-intermediate R users in
    mind and is optimized for user-friendliness. Advanced R users can already
    do everything covered here, but with janitor they can do it faster and save
    their thinking for the fun stuff."""

    cran = "janitor"

    license("MIT")

    version("2.2.0", sha256="29d5d0185e4e824bb38f905b158162a12f52dc01c2e8a487fc730ce46bf6baae")
    version("2.1.0", sha256="d60615940fbe174f67799c8abc797f27928eca4ac180418527c5897a4aaad826")
    version("1.2.0", sha256="5e15a2292c65c5ddd6160289dec2604b05a813651a2be0d7854ace4548a32b8c")
    version("1.1.1", sha256="404b41f56e571fab4c95ef62e79cb4f3bb34d5bb6e4ea737e748ff269536176b")
    version("0.3.0", sha256="5e4d8ef895ed9c7b8fa91aeb93e25c009366b4c5faaf3d02265f64b33d4a45f4")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r-dplyr@0.7.0:", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-hms", type=("build", "run"), when="@2.2.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@2.1.0:")
    depends_on("r-lubridate", type=("build", "run"), when="@2.1.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"), when="@1.1.0:")
    depends_on("r-rlang", type=("build", "run"), when="@1.1.0:")
    depends_on("r-stringi", type=("build", "run"), when="@2.1.0:")
    depends_on("r-stringr", type=("build", "run"), when="@2.1.0:")
    depends_on("r-snakecase@0.9.2:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-tidyselect@1.0.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("r-tidyr@0.7.0:", type=("build", "run"))
