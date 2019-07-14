# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTtr(RPackage):
    """Functions and data to construct technical trading rules with R."""

    homepage = "https://github.com/joshuaulrich/TTR"
    url      = "https://cran.r-project.org/src/contrib/TTR_0.23-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/TTR"

    version('0.23-3', sha256='2136032c7a2cd2a82518a4412fc655ecb16597b123dbdebe5684caef9f15261f')
    version('0.23-1', '35f693ac0d97e8ec742ebea2da222986')

    depends_on('r-xts', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
