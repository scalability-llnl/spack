# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgpubr(RPackage):
    """ggpubr: 'ggplot2' Based Publication Ready Plots"""

    homepage = "http://www.sthda.com/english/rpkgs/ggpubr"
    url      = "https://cloud.r-project.org/src/contrib/ggpubr_0.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggpubr"

    version('0.2.2', sha256='1c93dc6d1f08680dd00a10b6842445700d1fccb11f18599fbdf51e70c6b6b364')
    version('0.2.1', sha256='611e650da9bd15d7157fdcdc4e926fee3b88df3aba87410fdb1c8a7294d98d28')
    version('0.2', sha256='06c3075d8c452840662f5d041c3d966494b87254a52a858c849b9e1e96647766')
    version('0.1.2', sha256='9b4749fe1a6e0e4c5201a587c57c1b4bed34253f95ab4fb365f7e892b86003fe')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-ggrepel', type=('build', 'run'))
    depends_on('r-ggsci', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.1.2', type=('build', 'run'))
    depends_on('r-tidyr', when='@0.2:', type=('build', 'run'))
    depends_on('r-purrr', when='@0.2:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.1:', when='@0.2:', type=('build', 'run'))
    depends_on('r-cowplot', when='@0.2:', type=('build', 'run'))
    depends_on('r-ggsignif', when='@0.2:', type=('build', 'run'))
    depends_on('r-scales', when='@0.2:', type=('build', 'run'))
    depends_on('r-gridextra', when='@0.2:', type=('build', 'run'))
    depends_on('r-glue', when='@0.2:', type=('build', 'run'))
    depends_on('r-polynom', when='@0.2:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.2.2:', type=('build', 'run'))
