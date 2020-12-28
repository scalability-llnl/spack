# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScales(RPackage):
    """Graphical scales map data to aesthetics, and provide methods for
    automatically determining breaks and labels for axes and legends."""

    homepage = "https://github.com/hadley/scales"
    url      = "https://cloud.r-project.org/src/contrib/scales_0.5.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/scales"

    version('1.0.0', sha256='0c1f4a14edd336a404da34a3cc71a6a9d0ca2040ba19360c41a79f36e06ca30c')
    version('0.5.0', sha256='dbfcc0817c4ab8b8777ec7d68ebfe220177c193cfb5bd0e8ba5d365dbfe3e97d')
    version('0.4.1', sha256='642b88fb1fce7bac72a0038ce532b65b8a79dffe826fec25033cf386ab630cd3')
    version('0.4.0', sha256='851ef6136339b361b3f843fb73ea89f9112279b9cc126bdb38acde8d24c1c6a7')

    depends_on('r@2.13:', when='@:0.5.0', type=('build', 'run'))
    depends_on('r@3.1:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-dichromat', when='@:0.5.0', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.5.0', type=('build', 'run'))
    depends_on('r-munsell@0.5:', type=('build', 'run'))
    depends_on('r-labeling', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-viridislite', type=('build', 'run'))
