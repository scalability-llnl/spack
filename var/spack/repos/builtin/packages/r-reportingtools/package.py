# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReportingtools(RPackage):
    """Tools for making reports in various formats.

    The ReportingTools software package enables users to easily display
    reports of analysis results generated from sources such as microarray
    and sequencing data. The package allows users to create HTML pages that
    may be viewed on a web browser such as Safari, or in other formats
    readable by programs such as Excel. Users can generate tables with
    sortable and filterable columns, make and display plots, and link table
    entries to other data sources such as NCBI or larger plots within the
    HTML page. Using the package, users can also produce a table of contents
    page to link various reports together for a particular project that can
    be viewed in a web browser. For more examples, please visit our site:
    http:// research-pub.gene.com/ReportingTools."""

    bioc = "ReportingTools"

    version("2.40.0", commit="808af36aa9756be8c907a8669726c90dcd02c73c")
    version("2.38.0", commit="5c4971eebbaf3577ef20b74bf36c2db4e91561cc")
    version("2.36.0", commit="34122d4bde5ce43415f63f2e39e3a088c55282cc")
    version("2.34.0", commit="fb5aef0b6e1c6166d0f025d9e6ca60e54c68dbaf")
    version("2.30.0", commit="fb9aee416f38cfd308d6d7264ccbcda0467642a7")
    version("2.24.0", commit="d114c658affba9b682a37b4e2caf4341cf8da6cf")
    version("2.22.1", commit="dce6af6c6a1cddff077fe61368f2c13e5a0e7bab")
    version("2.20.0", commit="77e14ae13fdc16654300852dfd94e6cef58009da")
    version("2.17.3", commit="b2e379cd5b813d8ccca37ec25f0660deec943622")
    version("2.16.0", commit="b1aa0ea302da7f2993ce8087b1d09c11ddf03663")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-hwriter", type=("build", "run"))
    depends_on("r-category", type=("build", "run"))
    depends_on("r-gostats", type=("build", "run"))
    depends_on("r-limma@3.17.5:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-edger", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-pfam-db", type=("build", "run"))
    depends_on("r-gseabase", type=("build", "run"))
    depends_on("r-biocgenerics@0.1.6:", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("r-deseq2@1.3.41:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggbio", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
