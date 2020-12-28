# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIso(RPackage):
    """Linear order and unimodal order (univariate) isotonic regression;
    bivariate isotonic regression with linear order on both variables."""

    homepage = "https://cloud.r-project.org/package=Iso"
    url      = "https://cloud.r-project.org/src/contrib/Iso_0.0-17.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Iso"

    version('0.0-18', sha256='2d7e8c4452653364ee086d95cea620c50378e30acfcff129b7261e1756a99504')
    version('0.0-17', sha256='c007d6eaf6335a15c1912b0804276ff39abce27b7a61539a91b8fda653629252')

    depends_on('r@1.7.0:', type=('build', 'run'))
