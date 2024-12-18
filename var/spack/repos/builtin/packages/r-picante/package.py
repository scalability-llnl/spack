# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPicante(RPackage):
    """R tools for integrating phylogenies and ecology.

    Functions for phylocom integration, community analyses, null-models, traits
    and evolution. Implements numerous ecophylogenetic approaches including
    measures of community phylogenetic and trait diversity, phylogenetic
    signal, estimation of trait values for unobserved taxa, null models for
    community and phylogeny randomizations, and utility functions for data
    input/output and phylogeny plotting. A full description of package
    functionality and methods are provided by Kembel et al. (2010)
    <doi:10.1093/bioinformatics/btq166>."""

    cran = "picante"

    license("GPL-2.0-only")

    version("1.8.2", sha256="56565ca7f7c37f49c961372a816724967c21a4f5025cd69b8b671122bfdc4aa7")
    version("1.8", sha256="81a6308dbb53c9cdab30c1f9ac727abee76314351823b3a2142c21ed8e1498ad")
    version("1.7", sha256="75e4d73080db67e776562a1d58685438461cbde39af46900c7838da56aef0a62")
    version("1.6-2", sha256="4db3a5a0fe5e4e9197c96245195843294fbb8d0a324edcde70c6ab01276ab7ff")
    version("1.6-1", sha256="2708315b26737857a6729fd67bde06bc939930035c5b09a8bba472a593f24000")

    depends_on("c", type="build")  # generated

    depends_on("r-ape", type=("build", "run"))
    depends_on("r-vegan", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
