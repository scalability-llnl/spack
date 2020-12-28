# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClusterprofiler(RPackage):
    """statistical analysis and visualization of functional profiles for genes
       and gene clusters.

       This package implements methods to analyze and visualize functional
       profiles (GO and KEGG) of gene and gene clusters."""

    homepage = "https://bioconductor.org/packages/clusterProfiler"
    git      = "https://git.bioconductor.org/packages/clusterProfiler.git"

    version('3.12.0', commit='6ec88d10832bdfd938e9c065b377015eedb7eee2')
    version('3.10.1', commit='39927ef7ff6f97e27557bcf4147e2133b364fd3c')
    version('3.8.1', commit='81e1a7ac49e4713703c55f87f945b20de5e7ab36')
    version('3.6.0', commit='ff15e3dba69b93bc872d5f5d07821cd9ae20d829')
    version('3.4.4', commit='b86b00e8405fe130e439362651a5567736e2d9d7')

    depends_on('r@3.3.1:', type=('build', 'run'))
    depends_on('r-dose@3.1.3:', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-gosemsim@2.0.0:', when='@3.4.4:3.6.0', type=('build', 'run'))
    depends_on('r-gosemsim', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-rvcheck', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))

    depends_on('r-dose@3.3.2:', when='@3.6.0:', type=('build', 'run'))

    depends_on('r@3.4.0:', when='@3.8.1:', type=('build', 'run'))
    depends_on('r-dose@3.5.1:', when='@3.8.1:', type=('build', 'run'))
    depends_on('r-enrichplot@0.99.7:', when='@3.8.1:', type=('build', 'run'))
