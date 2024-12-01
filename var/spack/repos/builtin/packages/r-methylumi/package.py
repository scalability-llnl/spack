# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMethylumi(RPackage):
    """Handle Illumina methylation data.

    This package provides classes for holding and manipulating Illumina
    methylation data. Based on eSet, it can contain MIAME information, sample
    information, feature information, and multiple matrices of data. An
    "intelligent" import function, methylumiR can read the Illumina text files
    and create a MethyLumiSet. methylumIDAT can directly read raw IDAT files
    from HumanMethylation27 and HumanMethylation450 microarrays. Normalization,
    background correction, and quality control features for GoldenGate,
    Infinium, and Infinium HD arrays are also included."""

    bioc = "methylumi"

    version("2.46.0", commit="eb09e6508f1619c789d6b3091a8065cb6571cdac")
    version("2.44.0", commit="8f1f1f944993800da2776cb3240b4482c09429ad")
    version("2.42.0", commit="73e9c7fe1252c4ca20dc7b4e58decf04bf22d5e0")
    version("2.40.1", commit="211039225ca6fca9af75b8266f656161912ce10f")
    version("2.36.0", commit="5fb0b609f9c9181ac99f902745958774e5489606")
    version("2.32.0", commit="e2a29c1b214c0d43c7325d176f9ce41dcf8e2f9d")

    depends_on("r@2.13:", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-fdb-infiniummethylation-hg19@2.2.0:", type=("build", "run"))
    depends_on("r-minfi", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"), when="@2.36.0:")
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-illuminaio", type=("build", "run"))
    depends_on("r-genomicfeatures", type=("build", "run"), when="@2.40.1:")
