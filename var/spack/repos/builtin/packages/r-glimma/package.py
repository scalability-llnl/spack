# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlimma(RPackage):
    """Interactive HTML graphics.

       This package generates interactive visualisations for analysis of RNA-
       sequencing data using output from limma, edgeR or DESeq2 packages in an
       HTML page. The interactions are built on top of the popular static
       representations of analysis results in order to provide additional
       information."""

    homepage = "https://bioconductor.org/packages/Glimma"
    git      = "https://git.bioconductor.org/packages/Glimma.git"

    version('1.12.0', commit='d02174239fe0b47983d6947ed42a1a53b24caecb')
    version('1.10.1', commit='ffc7abc36190396598fadec5e9c653441e47be72')
    version('1.8.2', commit='7696aca2c023f74d244b6c908a6e7ba52bfcb34b')
    version('1.6.0', commit='57572996982806aa7ac155eedb97b03249979610')
    version('1.4.0', commit='c613c5334ed7868f36d5716b97fdb6234fb291f8')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-biobase', when='@1.4.0:1.6.0', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-scater', when='@1.4.0', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@1.6.0:', type=('build', 'run'))
