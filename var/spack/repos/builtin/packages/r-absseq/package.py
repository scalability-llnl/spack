# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAbsseq(RPackage):
    """ABSSeq: a new RNA-Seq analysis method based on modelling absolute
    expression differences.

    Inferring differential expression genes by absolute counts difference
    between two groups, utilizing Negative binomial distribution and
    moderating fold-change according to heterogeneity of dispersion across
    expression level."""

    bioc = "ABSSeq"

    version("1.54.0", commit="5e7de8c2a6532073012660f22243c9f7a5568ef6")
    version("1.52.0", commit="07038c047775e17d5d29909927d2143efb63e9cb")
    version("1.50.0", commit="4f384d04ebaae6ea0b56e5cff9a9dcdcb6c8afb0")
    version("1.48.0", commit="b237c967d44d075ca306c35e92df8b66a60ce72d")
    version("1.44.0", commit="c202b4a059021ed1228ccee7303c69b0aa4ca1ee")
    version("1.38.0", commit="b686d92f0f0efdb835982efe761d059bc24b34ce")
    version("1.36.0", commit="bd419072432cba4ef58b4b37b3c69c85d78b1c4a")
    version("1.34.1", commit="0c3a2514ef644c6e0de3714bc91959a302c9e006")
    version("1.32.3", commit="189d81c3d70f957bf50780f76a6ddcee499b4784")
    version("1.22.8", commit="a67ba49bc156a4522092519644f3ec83d58ebd6a")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
