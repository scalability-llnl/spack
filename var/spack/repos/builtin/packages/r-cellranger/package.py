# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCellranger(RPackage):
    """Translate Spreadsheet Cell Ranges to Rows and Columns.

    Helper functions to work with spreadsheets and the "A1:D10" style of cell
    range specification."""

    cran = "cellranger"

    license("MIT")

    version("1.1.0", sha256="5d38f288c752bbb9cea6ff830b8388bdd65a8571fd82d8d96064586bd588cf99")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-rematch", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
