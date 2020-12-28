# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuantreg(RPackage):
    """Estimation and inference methods for models of conditional quantiles:
        Linear and nonlinear parametric and non-parametric (total variation
        penalized) models for conditional quantiles of a univariate response
        and several methods for handling censored survival data. Portfolio
        selection methods based on expected shortfall risk are also
        included."""

    homepage = "https://cloud.r-project.org/package=quantreg"
    url      = "https://cloud.r-project.org/src/contrib/quantreg_5.29.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/quantreg"

    version('5.51', sha256='df1330d245f66ee6d924b209bd4c15d44ff8cce52667959ec0d299975428bdb1')
    version('5.42.1', sha256='4cc2b0883c52694e58fcfde83e30e4a54be9f4d9cbcf6138f6498cc8e0b3ccab')
    version('5.40', sha256='86e310a235009ab85635dfb8803c175f80a35892e237db2525c4ef37a98936eb')
    version('5.29', sha256='bb4638e8f295579afa5c40c4de7266a6ea9221436ba4ca802f94cdb43bf20f25')
    version('5.26', sha256='9d7403f7c5ee219ec155838648401a1c4915a46a74f5774a0f6876c537ef2c87')

    depends_on('r@2.6:', type=('build', 'run'))
    depends_on('r-sparsem', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-matrixmodels', type=('build', 'run'))
