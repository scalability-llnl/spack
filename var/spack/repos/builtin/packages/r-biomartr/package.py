# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiomartr(RPackage):
    """Genomic Data Retrieval.

    Perform large scale genomic data retrieval and functional annotation
    retrieval. This package aims to provide users with a standardized way to
    automate genome, proteome, 'RNA', coding sequence ('CDS'), 'GFF', and
    metagenome retrieval from 'NCBI RefSeq', 'NCBI Genbank', 'ENSEMBL',
    'ENSEMBLGENOMES', and 'UniProt' databases. Furthermore, an interface to the
    'BioMart' database (Smedley et al. (2009) <doi:10.1186/1471-2164-10-22>)
    allows users to retrieve functional annotation for genomic loci. In
    addition, users can download entire databases such as 'NCBI RefSeq' (Pruitt
    et al. (2007) <doi:10.1093/nar/gkl842>), 'NCBI nr', 'NCBI nt', 'NCBI
    Genbank' (Benson et al. (2013) <doi:10.1093/nar/gks1195>), etc. as well as
    'ENSEMBL' and 'ENSEMBLGENOMES' with only one command."""

    cran = "biomartr"

    license("GPL-2.0-only")

    version("1.0.7", sha256="9d1d5c51b61ee67ce7ca18afdb0a136ef5709d92d077d80163f9d52ee6c28645")
    version("1.0.2", sha256="7fd6cccd915aa39e593fb7591107ab9792d98a119dd42f3f666e5184f4e42743")
    version("0.9.2", sha256="d88085696e9c5614828602254c33f2cdd3bbfeebc2f21a705eee3cb961097c89")

    depends_on("r@3.1.1:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-biomart", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-data-table@1.9.4:", type=("build", "run"))
    depends_on("r-dplyr@0.3.0:", type=("build", "run"))
    depends_on("r-readr@0.2.2:", type=("build", "run"), when="@0.9.2:")
    depends_on("r-readr@1.4.0:", type=("build", "run"), when="@1.0.2:")
    depends_on("r-downloader@0.3:", type=("build", "run"))
    depends_on("r-rcurl@1.95-4.5:", type=("build", "run"))
    depends_on("r-xml@3.98-1.1:", type=("build", "run"))
    depends_on("r-httr@0.6.1:", type=("build", "run"))
    depends_on("r-stringr@0.6.2:", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("r-philentropy", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"), when="@1.0.2:")
    depends_on("r-fs", type=("build", "run"))
    depends_on("r-fs@1.3.1:", type=("build", "run"), when="@0.9.2")
