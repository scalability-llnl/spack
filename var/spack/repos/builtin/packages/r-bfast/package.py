# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBfast(RPackage):
    """bfast: Breaks For Additive Season and Trend (BFAST)"""

    homepage = "https://cloud.r-project.org/package=bfast"
    url      = "https://cloud.r-project.org/src/contrib/bfast_1.5.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bfast"

    version('1.5.7', sha256='01585fe8944d05ebdb13795214077bc1365f0c0372e2a1f7edb914356dace558')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-forecast', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
