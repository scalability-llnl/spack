# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdegenet(RPackage):
    """Exploratory Analysis of Genetic and Genomic Data.

    Toolset for the exploration of genetic and genomic data. Adegenet provides
    formal (S4) classes for storing and handling various genetic data,
    including genetic markers with varying ploidy and hierarchical population
    structure ('genind' class), alleles counts by populations ('genpop'), and
    genome-wide SNP data ('genlight'). It also implements original multivariate
    methods (DAPC, sPCA), graphics, statistical tests, simulation tools,
    distance and similarity measures, and several spatial methods. A range of
    both empirical and simulated datasets is also provided to illustrate
    various methods."""

    cran = "adegenet"

    license("GPL-2.0-or-later")

    version("2.1.10", sha256="ab62780ac1dd575d01f3e0869b34728a74b2ca2eaeeccb2f520007e9a578b163")
    version("2.1.8", sha256="80d72c3eefe077723dec91c98b7d46815b9659ab7196581d18b6e9d6c27f5025")
    version("2.1.6", sha256="7823de4933634cb887481fe4b12cf2faacbaa1b4b66939584d10fcb7ce2da26b")
    version("2.1.5", sha256="e4eee8c41dae6cb0841db74ec6f9adb2580873f3e313471f37df58324c1857f2")
    version("2.1.3", sha256="0790114ecb22642683b5be1f4b3a6a49856e06dc2f9e21b9cba4390c2257f6c6")
    version("2.1.1", sha256="3043fe5d731a38ff0e266f090dcda448640c3d0fd61934c76da32d082e5dce7a")
    version("2.1.0", sha256="7ee44061002b41164bbc09256307ab02e536f4f2ac03f36c7dc8f85f6af4639a")
    version("2.0.1", sha256="7eddf46e64f680d54d034b68c50900d9bd5bc2e08309d062e230121b7460bb10")

    depends_on("c", type="build")  # generated

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r-ade4", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-ape", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-seqinr", type=("build", "run"))
    depends_on("r-boot", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-dplyr@0.4.1:", type=("build", "run"))
    depends_on("r-vegan", type=("build", "run"))

    depends_on("r-spdep", type=("build", "run"), when="@:2.1.3")
