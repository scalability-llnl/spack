# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REllipse(RPackage):
    """Functions for Drawing Ellipses and Ellipse-Like Confidence Regions

    Contains various routines for drawing ellipses and ellipse-like confidence
    regions, implementing the plots described in Murdoch and Chow (1996), A
    graphical display of large correlation matrices, The American Statistician
    50, 178-180. There are also routines implementing the profile plots
    described in Bates and Watts (1988), Nonlinear Regression Analysis and its
    Applications."""

    homepage = "https://cloud.r-project.org/package=ellipse"
    url      = "https://cloud.r-project.org/src/contrib/ellipse_0.3-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ellipse"

    version('0.4.2', sha256='1719ce9a00b9ac4d56dbf961803085b892d3359726fda3567bb989ddfed9a5f2')
    version('0.4.1', sha256='1a9a9c52195b26c2b4d51ad159ab98aff7aa8ca25fdc6b2198818d1a0adb023d')
    version('0.3-8', sha256='508d474c142f0770c25763d6c8f8f8c9dcf8205afd42ffa22e6be1e0360e7f45')

    depends_on('r@2.0.0:', type=('build', 'run'))
