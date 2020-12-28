# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWgcna(RPackage):
    """WGCNA: Weighted Correlation Network Analysis"""

    homepage = "https://cloud.r-project.org/package=WGCNA"
    url      = "https://cloud.r-project.org/src/contrib/WGCNA_1.68.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/WGCNA/"

    version('1.68', sha256='0a04f15a20817f9260ae1896eda3be83a7f4855a27a348df85c7f4d376f1efe8')
    version('1.67', sha256='c9cc9989763b2c80835489eabd38d9ee35b204305044d115ca7c775a103f6824')
    version('1.64-1', sha256='961a890cda40676ba533cd6de2b1d4f692addd16363f874c82ba8b65dd2d0db6')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-dynamictreecut@1.62:', type=('build', 'run'))
    depends_on('r-fastcluster', type=('build', 'run'))
    depends_on('r-matrixstats@0.8.1:', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-impute', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-robust', type=('build', 'run'))
