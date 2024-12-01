# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyqcreport(RPackage):
    """QC Report Generation for affyBatch objects.

    This package creates a QC report for an AffyBatch object. The report is
    intended to allow the user to quickly assess the quality of a set of
    arrays in an AffyBatch object."""

    bioc = "affyQCReport"

    version("1.68.0", commit="34b42a16f87a90a595146f4a1802ed04f6bfccca")
    version("1.62.0", commit="92d4124b688b90a6a9b8a21ab9d13d92b368cee4")
    version("1.60.0", commit="d0c15b1c56fc1caf6f114877ea6c1b8483a0dcfa")
    version("1.58.0", commit="14be93a1e7a6d1a64c38ed2f53e0c52a389b2a1b")
    version("1.56.0", commit="5c824045c7364155eafc2dd5bb342374aa1ca072")
    version("1.54.0", commit="5572e9981dc874b78b4adebf58080cac3fbb69e1")

    depends_on("r-biobase@1.13.16:", type=("build", "run"))
    depends_on("r-affy", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-affyplm", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"), when="@1.68.0:")
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-simpleaffy", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
