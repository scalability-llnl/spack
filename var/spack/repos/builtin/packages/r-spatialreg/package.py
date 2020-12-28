# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatialreg(RPackage):
    """spatialreg: Spatial Regression Analysis"""

    homepage = "https://cloud.r-project.org/package=spatialreg"
    url      = "https://cloud.r-project.org/src/contrib/spatialreg_1.1-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatialreg"

    version('1.1-3', sha256='7609cdfcdfe427d2643a0db6b5360be3f6d60ede8229436ab52092d1c9cf0480')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-gmodels', type=('build', 'run'))
    depends_on('r-learnbayes', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-spdata', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
