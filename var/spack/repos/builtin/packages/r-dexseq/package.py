# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDexseq(RPackage):
    """Inference of differential exon usage in RNA-Seq.

    The package is focused on finding differential exon usage using RNA-seq
    exon counts between samples with different experimental designs. It
    provides functions that allows the user to make the necessary
    statistical tests based on a model that uses the negative binomial
    distribution to estimate the variance between biological replicates
    and generalized linear models for testing. The package also provides
    functions for the visualization and exploration of the results."""

    bioc = "DEXSeq"

    maintainers("dorton21")

    version("1.46.0", commit="074c0bf6776eea69e58a788a0f6904dd632a1b74")
    version("1.44.0", commit="9660d7372d5ced1a7e324ed9a61b935023b7d135")
    version("1.42.0", commit="d91de62a27d0cab2ef12ef1a5f23dc2f7a0cfadd")
    version("1.40.0", commit="7d2d639b3a157e443058fc557132cd2629bb36f3")
    version("1.36.0", commit="f0a361af6954fcc2abb2db801c26e303570669b2")

    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-iranges@2.5.17:", type=("build", "run"))
    depends_on("r-genomicranges@1.23.7:", type=("build", "run"))
    depends_on("r-deseq2@1.9.11:", type=("build", "run"))
    depends_on("r-deseq2@1.39.6:", type=("build", "run"), when="@1.46.0:")
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-s4vectors@0.23.18:", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-biomart", type=("build", "run"))
    depends_on("r-hwriter", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-statmod", type=("build", "run"))
    depends_on("r-geneplotter", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
