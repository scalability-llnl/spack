# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPl94171(RPackage):
    """Tabulate P.L. 94-171 Redistricting Data Summary Files

    Tools to process legacy format summary redistricting data files produced by
    the United States Census Bureau pursuant to P.L. 94-171. These files are
    generally available earlier but are difficult to work with as-is."""

    homepage = "https://corymccartan.com/PL94171/"
    cran = "PL94171"

    maintainers("jgaeb")

    version("1.1.2", sha256="53ca90801eb04a0535dda0f98869fe1d7f67e40702e5f77570303bbbb5289c73")
    version("1.1.1", sha256="a4016b94070c9e811f33ee7f0b662d968d250391848b8afd7f7386c625b6c2fe")
    version("1.0.2", sha256="3cbe058ab8f99944dd7b034ba93044d03d8351c3036759d8980378f78bef0330")
    version("1.0.1", sha256="c31ccf045a742719efe94fa08109b52c6a986d86d15815041fb93c877cf5f474")
    version("0.3.2", sha256="9135e4a1405e90ae7855af568794eb71702a3142d3ab089702061a359e9bba1e")
    version("0.2.0", sha256="8d4cf1199812dacfc9a62b975056ba3c763a899bfc177e48f059581a3e4550e1")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-readr", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-tigris", type=("build", "run"), when="@0.2.0:1.0.2")
    depends_on("r-tinytiger", type=("build", "run"), when="@1.1.1:")
    depends_on("r-cli", type=("build", "run"), when="@1.1.1:")
