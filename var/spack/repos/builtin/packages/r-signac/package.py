# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSignac(RPackage):
    """Analysis of Single-Cell Chromatin Data.

    A framework for the analysis and exploration of single-cell chromatin data.
    The 'Signac' package contains functions for quantifying single-cell
    chromatin data, computing per-cell quality control metrics, dimension
    reduction and normalization, visualization, and DNA sequence motif
    analysis. Reference: Stuart et al. (2021)
    <doi:10.1038/s41592-021-01282-5>."""

    cran = "Signac"

    version("1.14.0", sha256="e0aad9e2c27c148fdd376081c2de1e3db46b1835eac83ef41fe562e08363c59e")
    version("1.9.0", sha256="b8ff36427e5919fd420daa1f50cf8c71935293ee7f88560041acb993b5e3afa8")
    version("1.8.0", sha256="9c4b123f4d077111c7e6dd1659483ada984300c8e923672ca924e46fb6a1dd06")
    version("1.7.0", sha256="5e4456eeab29fa2df7f6236b050dec8cb9c073d7652a89ee5030a27f94e5e4bf")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r@4.1.0:", type=("build", "run"), when="@1.14.0:")
    depends_on("r-genomeinfodb@1.29.3:", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-seuratobject@4.0.0:", type=("build", "run"))
    depends_on("r-seuratobject@5.0.2:", type=("build", "run"), when="@1.14.0:")
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"))
    depends_on("r-future", type=("build", "run"))
    depends_on("r-future-apply", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.10.0:")
    depends_on("r-irlba", type=("build", "run"))
    depends_on("r-pbapply", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-patchwork", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-stringi", type=("build", "run"))
    depends_on("r-fastmatch", type=("build", "run"))
    depends_on("r-rcpproll", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.12.0:")
    depends_on("zlib-api")
