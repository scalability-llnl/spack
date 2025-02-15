# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVcfr(RPackage):
    """Manipulate and Visualize VCF Data.

    Facilitates easy manipulation of variant call format (VCF) data. Functions
    are provided to rapidly read from and write to VCF files. Once VCF data is
    read into R a parser function extracts matrices of data. This information
    can then be used for quality control or other purposes. Additional
    functions provide visualization of genomic data. Once processing is
    complete data may be written to a VCF file (*.vcf.gz). It also may be
    converted into other popular R objects (e.g., genlight, DNAbin). VcfR
    provides a link between VCF data and familiar R software."""

    cran = "vcfR"

    maintainers("dorton21")

    version("1.15.0", sha256="df17e48b961d96f2a78a1a15037df674f57d0445f2669e401543d8082f0b49fa")
    version("1.14.0", sha256="8576dbd2e5a707dabc20acbbea3fe18b6a783910e622423ac203609a386204cb")
    version("1.13.0", sha256="743ce845732ada638f0f8a2cd789cd06aa25d818fec87c8bdb998f7c77089ebc")
    version("1.12.0", sha256="dd87ff010365de363864a44ca49887c0fdad0dd18d0d9c66e44e39c2d4581d52")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-memuse", type=("build", "run"))
    depends_on("r-pinfsc50", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-vegan", type=("build", "run"))
    depends_on("r-viridislite", type=("build", "run"))
    depends_on("zlib-api")
