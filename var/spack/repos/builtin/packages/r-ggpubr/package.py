# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgpubr(RPackage):
    """ggpubr: 'ggplot2' Based Publication Ready Plots"""

    homepage = "http://www.sthda.com/english/rpkgs/ggpubr"
    url      = "https://cloud.r-project.org/src/contrib/ggpubr_0.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggpubr"

    version('0.2', sha256='06c3075d8c452840662f5d041c3d966494b87254a52a858c849b9e1e96647766')
    version('0.1.2', '42a5749ae44121597ef511a7424429d1')

    depends_on('r@3.1.0:')
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
