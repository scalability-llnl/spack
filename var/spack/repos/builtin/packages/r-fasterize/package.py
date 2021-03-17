# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFasterize(RPackage):
    """Provides drop-in replacement for rasterize() from the package raster."""

    homepage = "https://cran.r-project.org/package=fasterize"
    url      = "https://cran.r-project.org/src/contrib/fasterize_1.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fasterize/"

    version('1.0.3', sha256='62b459625e9bdb00251ec5f6cb873e0c59713f3e86dc1e2c8332adc0cea17f81')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
