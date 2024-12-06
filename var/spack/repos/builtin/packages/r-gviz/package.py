# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGviz(RPackage):
    """Plotting data and annotation information along genomic coordinates.

    Genomic data analyses requires integrated visualization of known genomic
    information and new experimental data. Gviz uses the biomaRt and the
    rtracklayer packages to perform live annotation queries to Ensembl and
    UCSC and translates this to e.g. gene/transcript structures in viewports
    of the grid graphics package. This results in genomic information
    plotted together with your data."""

    bioc = "Gviz"

    license("Artistic-2.0")

    version("1.44.0", commit="e70aaa7dd27df8482ee854395475a87ec2121279")
    version("1.42.0", commit="4eddb688bca3fdeb65fd536d653d7ba7f7976121")
    version("1.40.1", commit="d21843710cd05135353de5cd4ce4d35cdd333b7c")
    version("1.38.3", commit="c4b352a16455a5744533c511e59354977814cb9e")
    version("1.34.0", commit="445fadff2aedd8734580fa908aa47ff1216a8182")
    version("1.28.3", commit="20b9825af144cfc888629c34aa980b5bbd65bf86")
    version("1.26.5", commit="430310b9d2e098f9757a71d26a2f69871071f30c")
    version("1.24.0", commit="3ee1eec97a56653c07c434a97f82cfe3c4281841")
    version("1.22.3", commit="2238079d0a7017c474f010acb35d98ee7cc1c5d1")
    version("1.20.0", commit="299b8255e1b03932cebe287c3690d58c88f5ba5c")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@1.34.0:")
    depends_on("r@4.1:", type=("build", "run"), when="@1.38.3:")
    depends_on("r@4.2:", type=("build", "run"), when="@1.40.1:")
    depends_on("r@4.3:", type=("build", "run"), when="@1.44.0:")
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-iranges@1.99.18:", type=("build", "run"))
    depends_on("r-genomicranges@1.17.20:", type=("build", "run"))
    depends_on("r-xvector@0.5.7:", type=("build", "run"))
    depends_on("r-rtracklayer@1.25.13:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-biomart@2.11.0:", type=("build", "run"))
    depends_on("r-annotationdbi@1.27.5:", type=("build", "run"))
    depends_on("r-biobase@2.15.3:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.17.22:", type=("build", "run"))
    depends_on("r-ensembldb@2.11.3:", type=("build", "run"), when="@1.34.0:")
    depends_on("r-bsgenome@1.33.1:", type=("build", "run"))
    depends_on("r-biostrings@2.33.11:", type=("build", "run"))
    depends_on("r-biovizbase@1.13.8:", type=("build", "run"))
    depends_on("r-rsamtools@1.17.28:", type=("build", "run"))
    depends_on("r-latticeextra@0.6-26:", type=("build", "run"))
    depends_on("r-matrixstats@0.8.14:", type=("build", "run"))
    depends_on("r-genomicalignments@1.1.16:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.1.3:", type=("build", "run"))
    depends_on("r-biocgenerics@0.11.3:", type=("build", "run"))
    depends_on("r-digest@0.6.8:", type=("build", "run"))
