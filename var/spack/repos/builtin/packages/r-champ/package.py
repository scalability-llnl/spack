# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChamp(RPackage):
    """Chip Analysis Methylation Pipeline for Illumina HumanMethylation450 and
    EPIC.

    The package includes quality control metrics, a selection of
    normalization methods and novel methods to identify differentially
    methylated regions and to highlight copy number alterations."""

    bioc = "ChAMP"

    version("2.30.0", commit="b6ff6670d239c2517aa57144a793ea93da3c7b42")
    version("2.28.0", commit="3d27ac67a738afea8cc9ece6ea1301120e4b48f7")
    version("2.26.0", commit="1548910bf53e1e5f7a8d80c83b742a94297d8a34")
    version("2.24.0", commit="7ba19da74b61e1c40ced162ba753f0f9b9c7647a")
    version("2.20.1", commit="99ea0463bce59f5b06bcc91f479dcd4065074896")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-minfi", type=("build", "run"))
    depends_on("r-champdata@2.6.0:", type=("build", "run"))
    depends_on("r-dmrcate", type=("build", "run"))
    depends_on("r-illumina450probevariants-db", type=("build", "run"))
    depends_on("r-illuminahumanmethylationepicmanifest", type=("build", "run"))
    depends_on("r-dt", type=("build", "run"))
    depends_on("r-rpmm", type=("build", "run"))
    depends_on("r-prettydoc", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"))
    depends_on("r-globaltest", type=("build", "run"))
    depends_on("r-sva", type=("build", "run"))
    depends_on("r-illuminaio", type=("build", "run"))
    depends_on("r-rmarkdown", type=("build", "run"))
    depends_on("r-illuminahumanmethylation450kmanifest", type=("build", "run"))
    depends_on("r-illuminahumanmethylationepicanno-ilm10b4-hg19", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-dnacopy", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-impute", type=("build", "run"))
    depends_on("r-marray", type=("build", "run"))
    depends_on("r-watermelon", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-goseq", type=("build", "run"))
    depends_on("r-missmethyl", type=("build", "run"))
    depends_on("r-kpmt", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-qvalue", type=("build", "run"))
    depends_on("r-isva", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-bumphunter", type=("build", "run"))
    depends_on("r-quadprog", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"))
    depends_on("r-shinythemes", type=("build", "run"))
    depends_on("r-plotly@4.5.6:", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-dendextend", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-combinat", type=("build", "run"))
