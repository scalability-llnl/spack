# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RKs(RPackage):
    """Kernel Smoothing

    Kernel smoothers for univariate and multivariate data, including densities,
    density derivatives, cumulative distributions, clustering, classification,
    density ridges, significant modal regions, and two-sample hypothesis tests.
    Chacon & Duong (2018) <doi:10.1201/9780429485572>."""

    homepage = "https://cloud.r-project.org/package=ks"
    url      = "https://cloud.r-project.org/src/contrib/ks_1.11.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ks"

    version('1.11.7', sha256='6a6d9c2366e85a4c6af39b798f3798d20a42615ddfcebcedf6cf56087cdfd2b8')
    version('1.11.5', sha256='4f65565376391b8a6dcce76168ef628fd4859dba8496910cbdd54e4f88e8d51b')
    version('1.11.4', sha256='0beffaf8694819fba8c93af07a8782674a15fe00a04ad1d94d31238d0a41b134')
    version('1.11.2', sha256='9dfd485096e1e67abc7dfcb7b76a83de110dd15bcfeffe5c899605b3a5592961')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-fnn@1.1:', type=('build', 'run'))
    depends_on('r-kernlab', type=('build', 'run'))
    depends_on('r-kernsmooth@2.22:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-multicool', type=('build', 'run'))
    depends_on('r-mvtnorm@1.0-0:', type=('build', 'run'))
