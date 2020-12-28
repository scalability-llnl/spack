# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTseries(RPackage):
    """Time series analysis and computational finance."""

    homepage = "https://cloud.r-project.org/package=tseries"
    url      = "https://cloud.r-project.org/src/contrib/tseries_0.10-42.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tseries"

    version('0.10-47', sha256='202377df56806fe611c2e12c4d9732c71b71220726e2defa7e568d2b5b62fb7b')
    version('0.10-46', sha256='12940afd1d466401160e46f993ed4baf28a42cef98d3757b66ee15e916e07222')
    version('0.10-42', sha256='827f79858715c700e8cabd2c27853ba88ad0e05eb043bc94e126b155a75546c4')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-quadprog', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-quantmod@0.4-9:', type=('build', 'run'))
