# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYarn(RPackage):
    """Robust Multi-Condition RNA-Seq Preprocessing and Normalization.

    Expedite large RNA-Seq analyses using a combination of previously
    developed tools. YARN is meant to make it easier for the user in
    performing basic mis-annotation quality control, filtering, and
    condition-aware normalization. YARN leverages many Bioconductor tools
    and statistical techniques to account for the large heterogeneity and
    sparsity found in very large RNA-seq experiments."""

    bioc = "yarn"

    version("1.26.0", commit="54dac4a6afe6b036bac60482cf268aa0cf28cec4")
    version("1.24.0", commit="d3a9c5cc1f97bff111dc9332f32ded676e3709d3")
    version("1.22.0", commit="0d94152eee4224bf1ca467fad7f2b35c2e1df6b2")
    version("1.20.0", commit="b41e4ef14f980518af2fc59f202ad8ec148e8b47")
    version("1.16.0", commit="ff5a18cb946ffec3cb773fe32af401c8a72d674a")
    version("1.10.0", commit="36ffe84148eb871e93bc8f9e697475319b5ea472")
    version("1.8.1", commit="ee0723d4dbf082b4469ca9c22cce4f1a2ac81c04")
    version("1.6.0", commit="19d1b2ef275f294bd318b86e0d237c271880117d")
    version("1.4.0", commit="36100f40b9e520c072d0d5ebf963723b813f7db0")
    version("1.2.0", commit="28af616ef8c27dcadf6568e276dea8465486a697")

    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biomart", type=("build", "run"))
    depends_on("r-downloader", type=("build", "run"))
    depends_on("r-edger", type=("build", "run"))
    depends_on("r-gplots", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-readr", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-quantro", type=("build", "run"))
