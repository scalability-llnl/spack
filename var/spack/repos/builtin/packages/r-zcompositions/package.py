# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RZcompositions(RPackage):
    """Treatment of Zeros, Left-Censored and Missing Values in Compositional
    Data Sets

    Principled methods for the imputation of zeros, left-censored and missing
    data in compositional data sets (Palarea-Albaladejo and Martin-Fernandez
    (2015) <doi:10.1016/j.chemolab.2015.02.019>)."""

    homepage = "https://cloud.r-project.org/package=zCompositions"
    url      = "https://cloud.r-project.org/src/contrib/zCompositions_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/zCompositions"

    version('1.3.4', sha256='ae22c86fe92368a26265933f42eecc518b9b69e7d9b698bc31bfaabfc3c48e95')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-nada', type=('build', 'run'))
    depends_on('r-truncnorm', type=('build', 'run'))
