# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCircstats(RPackage):
    """Circular Statistics, from Topics in Circular Statistics"""

    homepage = "https://cran.r-project.org/package=CircStats"
    url      = "https://cran.r-project.org/src/contrib/CircStats_0.2-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/CircStats/"

    version('0.2-6', sha256='8efed93b75b314577341effea214e3dd6e0a515cfe1212eb051047a1f3276f1d')

    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
