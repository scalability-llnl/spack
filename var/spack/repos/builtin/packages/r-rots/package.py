# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRots(RPackage):
    """Reproducibility-Optimized Test Statistic.

       Calculates the Reproducibility-Optimized Test Statistic (ROTS) for
       differential testing in omics data."""

    homepage = "https://bioconductor.org/packages/ROTS"
    git      = "https://git.bioconductor.org/packages/ROTS.git"

    version('1.12.0', commit='7e2c96fd8fd36710321498745f24cc6b59ac02f0')
    version('1.10.1', commit='1733d3f868cef4d81af6edfc102221d80793937b')
    version('1.8.0', commit='02e3c6455bb1afe7c4cc59ad6d4d8bae7b01428b')
    version('1.6.0', commit='3567ac1142ba97770b701ee8e5f9e3e6c781bd56')
    version('1.4.0', commit='2e656514a4bf5a837ee6e14ce9b28a61dab955e7')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
