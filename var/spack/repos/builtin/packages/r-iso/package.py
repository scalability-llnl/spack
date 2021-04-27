# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RIso(RPackage):
    """Functions to Perform Isotonic Regression

    Linear order and unimodal order (univariate) isotonic regression;
    bivariate isotonic regression with linear order on both variables."""

    homepage = "https://cloud.r-project.org/package=Iso"
    url      = "https://cloud.r-project.org/src/contrib/Iso_0.0-17.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Iso"

    version('0.0-18.1', sha256='2fa5f78a7603cbae94a5e38e791938596a053d48c609a7c120a19cbb7d93c66f')
    version('0.0-18', sha256='2d7e8c4452653364ee086d95cea620c50378e30acfcff129b7261e1756a99504')
    version('0.0-17', sha256='c007d6eaf6335a15c1912b0804276ff39abce27b7a61539a91b8fda653629252')

    depends_on('r@1.7.0:', type=('build', 'run'))
