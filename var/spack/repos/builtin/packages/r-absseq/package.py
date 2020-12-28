# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://bioconductor.org/packages/ABSSeq"
    git      = "https://git.bioconductor.org/packages/ABSSeq.git"

    version('1.38.0', commit='b686d92f0f0efdb835982efe761d059bc24b34ce')
    version('1.36.0', commit='bd419072432cba4ef58b4b37b3c69c85d78b1c4a')
    version('1.34.1', commit='0c3a2514ef644c6e0de3714bc91959a302c9e006')
    version('1.32.3', commit='189d81c3d70f957bf50780f76a6ddcee499b4784')
    version('1.22.8', commit='a67ba49bc156a4522092519644f3ec83d58ebd6a')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
