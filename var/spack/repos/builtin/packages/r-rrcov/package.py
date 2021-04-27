# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRrcov(RPackage):
    """Scalable Robust Estimators with High Breakdown Point

    Robust Location and Scatter Estimation and Robust Multivariate Analysis
    with High Breakdown Point: principal component analysis (Filzmoser and
    Todorov (2013), <doi:10.1016/j.ins.2012.10.017>), linear and quadratic
    discriminant analysis (Todorov and Pires (2007)), multivariate tests
    (Todorov and Filzmoser (2010) <doi:10.1016/j.csda.2009.08.015>), outlier
    detection (Todorov et al. (2010) <doi:10.1007/s11634-010-0075-2>). See also
    Todorov and Filzmoser (2009) <ISBN-13:978-3838108148>, Todorov and
    Filzmoser (2010) <doi:10.18637/jss.v032.i03> and Boudt et al. (2019)
    <doi:10.1007/s11222-019-09869-x>."""

    homepage = "https://cloud.r-project.org/package=rrcov"
    url      = "https://cloud.r-project.org/src/contrib/rrcov_1.4-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rrcov"

    version('1.5-5', sha256='1f7f07558e347e7d1f1adff68631764670bc672777a7d990901c4fa94cc0e629')
    version('1.4-7', sha256='cbd08ccce8b583a2f88946a3267c8fc494ee2b44ba749b9296a6e3d818f6f293')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-robustbase@0.92.1:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
    depends_on('r-cluster', when='@:1.4-7', type=('build', 'run'))
