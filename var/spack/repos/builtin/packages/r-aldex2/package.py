# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAldex2(RPackage):
    """Analysis Of Differential Abundance Taking Sample Variation Into Account.

       A differential abundance analysis for the comparison of two or more
       conditions. Useful for analyzing data from standard RNA-seq or meta-RNA-
       seq assays as well as selected and unselected values from in-vitro
       sequence selections. Uses a Dirichlet-multinomial model to infer
       abundance from counts, optimized for three or more experimental
       replicates. The method infers biological and sampling variation to
       calculate the expected false discovery rate, given the variation, based
       on a Wilcoxon Rank Sum test and Welch's t-test (via aldex.ttest), a
       Kruskal-Wallis test (via aldex.kw), a generalized linear model (via
       aldex.glm), or a correlation test (via aldex.corr). All tests report
       p-values and Benjamini-Hochberg corrected p-values."""

    homepage = "https://bioconductor.org/packages/ALDEx2"
    git      = "https://git.bioconductor.org/packages/ALDEx2.git"

    version('1.16.0', commit='bd698a896a5bea91187e3060e56a147bad1d586f')
    version('1.14.1', commit='a8b970c594a00a37c064227bf312d5f89dccabe8')
    version('1.12.0', commit='9efde428d22a0be1fe7b6655d45ddce8fcded180')
    version('1.10.0', commit='e43f99e4009ad4d5ed200cc8a19faf7091c0c98a')
    version('1.8.0', commit='24104824ca2402ad4f54fbf1ed9cee7fac2aaaf1')

    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))

    depends_on('r-multtest', when='@1.10.0:', type=('build', 'run'))
