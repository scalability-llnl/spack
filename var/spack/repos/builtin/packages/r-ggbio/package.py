# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgbio(RPackage):
    """Visualization tools for genomic data.

    The ggbio package extends and specializes the grammar of graphics for
    biological data. The graphics are designed to answer common scientific
    questions, in particular those often asked of high throughput genomics
    data. All core Bioconductor data structures are supported, where
    appropriate. The package supports detailed views of particular genomic
    regions, as well as genome-wide overviews. Supported overviews include
    ideograms and grand linear views. High-level plots include sequence
    fragment length, edge-linked interval to data view, mismatch pileup, and
    several splicing summaries."""

    bioc = "ggbio"

    version("1.48.0", commit="fd4ebca44151e8f8e20ad2a38292398a3a4bb948")
    version("1.46.0", commit="d9c6cb495c7268bcaaab141231a9038aec8498bc")
    version("1.44.1", commit="0301d9464e304a8113ea4479185cd358855ca365")
    version("1.44.0", commit="cb21284a9803917fa76e116adfc456525c95f660")
    version("1.42.0", commit="3540047ef018957d59fba8af7d3c58e4659f8e26")
    version("1.38.0", commit="c39c51993f419cfc2f094e664477f25f5212a242")
    version("1.32.0", commit="04bd12fbe0b1c5c6b721a5f927e1352765f9bf88")
    version("1.30.0", commit="8b05258b089b06a743352e92058edda06c24cfb7")
    version("1.28.5", commit="594521ca556ef7d97cf4882ecfa54d22c2a2faba")
    version("1.26.1", commit="b4f4c898c92aa1082aa7574f1e5c2a0dae943fbc")
    version("1.24.1", commit="ef04c1bca1330f37152bcc21080cbde94849a094")

    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-ggplot2@1.0.0:", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-gtable", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"))
    depends_on("r-biovizbase@1.23.3:", type=("build", "run"))
    depends_on("r-biovizbase@1.28.2:", type=("build", "run"), when="@1.28.5:")
    depends_on("r-biovizbase@1.29.2:", type=("build", "run"), when="@1.30.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-s4vectors@0.13.13:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-iranges@2.11.16:", type=("build", "run"), when="@1.26.1:")
    depends_on("r-genomeinfodb@1.1.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.21.10:", type=("build", "run"))
    depends_on("r-genomicranges@1.29.14:", type=("build", "run"), when="@1.26.1:")
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-rsamtools@1.17.28:", type=("build", "run"))
    depends_on("r-genomicalignments@1.1.16:", type=("build", "run"))
    depends_on("r-bsgenome", type=("build", "run"))
    depends_on("r-variantannotation@1.11.4:", type=("build", "run"))
    depends_on("r-rtracklayer@1.25.16:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.17.13:", type=("build", "run"))
    depends_on("r-genomicfeatures@1.29.11:", type=("build", "run"), when="@1.26.1:")
    depends_on("r-organismdbi", type=("build", "run"))
    depends_on("r-ggally", type=("build", "run"))
    depends_on("r-ensembldb@1.99.13:", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-annotationfilter", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.28.5:")
