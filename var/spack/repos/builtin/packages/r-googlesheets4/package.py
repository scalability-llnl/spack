# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGooglesheets4(RPackage):
    """Access Google Sheets using the Sheets API V4.

    Interact with Google Sheets through the Sheets API v4
    <https://developers.google.com/sheets/api>. "API" is an acronym for
    "application programming interface"; the Sheets API allows users to
    interact with Google Sheets programmatically, instead of via a web browser.
    The "v4" refers to the fact that the Sheets API is currently at version 4.
    This package can read and write both the metadata and the cell data in a
    Sheet."""

    cran = "googlesheets4"

    license("MIT")

    version("1.1.0", sha256="50e15543bef5b8d8cda36f6ea8a1d59b256d889cd3cedddc91f00ae30c8c8ec9")
    version("1.0.1", sha256="284ecbce98944093cb065c1b0b32074eae7b45fd74b87d7815c7ca6deca76591")
    version("1.0.0", sha256="0a107d76aac99d6db48d97ce55810c1412b2197f457b8476f676169a36c7cc7a")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.0.1:")
    depends_on("r@3.5:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-cellranger", type=("build", "run"))
    depends_on("r-cli@3.0.0:", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-gargle@1.2.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-gargle@1.3.0:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-googledrive@2.0.0:", type=("build", "run"))
    depends_on("r-googledrive@2.1.0:", type=("build", "run"), when="@1.1.0:")
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-ids", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.1.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-rematch2", type=("build", "run"))
    depends_on("r-rlang@0.4.11:", type=("build", "run"))
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@1.0.1:")
    depends_on("r-tibble@2.1.1:", type=("build", "run"))
    depends_on("r-vctrs@0.2.3:", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"), when="@1.1.0:")
