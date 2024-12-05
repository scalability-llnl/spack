# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpadesAddins(RPackage):
    """Development Tools for 'SpaDES' and 'SpaDES' Modules.

    Provides 'RStudio' addins for 'SpaDES' packages and 'SpaDES' module
    development. See '?SpaDES.addins' for an overview of the tools provided."""

    cran = "SpaDES.addins"

    maintainers("dorton21")

    version("0.1.4", sha256="d4c0f0a4641febb501e9e17d1b771bd857ca8edd024845351895e5927c08c453")
    version("0.1.3", sha256="b77aef21d1c725f855fe6f03456187d3c8b8070d56d80b7e6733979b644e162e")
    version("0.1.2", sha256="0a16bd9423797a4b4ed66a5e669cdd7f6984a3f30aa1aadc078678ee2622367c")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@3.6:", type=("build", "run"), when="@0.1.3:")
    depends_on("r@4.0:", type=("build", "run"), when="@0.1.4:")
    depends_on("r-devtools", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-miniui@0.1.1:", type=("build", "run"))
    depends_on("r-reproducible", type=("build", "run"))
    depends_on("r-rstudioapi@0.5:", type=("build", "run"))
    depends_on("r-shiny@0.13:", type=("build", "run"))
    depends_on("r-spades-core", type=("build", "run"))
    depends_on("r-stringi@1.1.3:", type=("build", "run"))
