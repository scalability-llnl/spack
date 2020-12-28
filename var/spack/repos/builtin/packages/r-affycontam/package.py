# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycontam(RPackage):
    """structured corruption of affymetrix cel file data.

       structured corruption of cel file data to demonstrate QA
       effectiveness"""

    homepage = "https://bioconductor.org/packages/affyContam"
    git      = "https://git.bioconductor.org/packages/affyContam.git"

    version('1.42.0', commit='8a5e94a5ae8c2ecfafa6177b84a6e8ab07e14fbe')
    version('1.40.0', commit='dfd5fd6ae04941dddbda03f656540b71b2fbc614')
    version('1.38.0', commit='84651e8eade61619afefc83bb290047da101a5bc')
    version('1.36.0', commit='aeb684a7d3f6fa9243f3946d214de53649fa4fd6')
    version('1.34.0', commit='03529f26d059c19e069cdda358dbf7789b6d4c40')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-affydata', type=('build', 'run'))
