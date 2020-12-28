# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFactoextra(RPackage):
    """factoextra: Extract and Visualize the Results of Multivariate Data
    Analyses"""

    homepage = "http://www.sthda.com/english/rpkgs/factoextra"
    url      = "https://cloud.r-project.org/src/contrib/factoextra_1.0.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/factoextra"

    version('1.0.5', sha256='8177a3f5107883ae248b2cd0afa388a1794741f5155a9455b3883788cf44d5d0')
    version('1.0.4', sha256='e4a000a04ef5b9aa0790dc6e5277451c482a19ba10dda9474f6c6982424aeed3')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.0:', type=('build', 'run'))
    depends_on('r-abind', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-dendextend', type=('build', 'run'))
    depends_on('r-factominer', type=('build', 'run'))
    depends_on('r-ggpubr@0.1.5:', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
