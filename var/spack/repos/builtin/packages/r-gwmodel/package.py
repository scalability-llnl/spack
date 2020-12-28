# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGwmodel(RPackage):
    """GWmodel: Geographically-Weighted Models"""

    homepage = "http://gwr.nuim.ie/"
    url      = "https://cloud.r-project.org/src/contrib/GWmodel_2.0-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GWmodel"

    version('2.1-3', sha256='3e1a36fddf8e64f61d548067bb043216f8d12069d814a4cbf07a9cae0b310af6')
    version('2.1-1', sha256='91241b4e26d423a54c7c6784ef5159759058a5dafdff18a1ea8451faf979d1f3')
    version('2.0-9', sha256='b479af2c19d4aec30f1883d00193d52e342c609c1badcb51cc0344e4404cffa7')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-maptools@0.5-2:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-spacetime', type=('build', 'run'))
    depends_on('r-spatialreg', type=('build', 'run'))
    depends_on('r-spdep', type=('build', 'run'))
    depends_on('r-fnn', when='@2.1-1:', type=('build', 'run'))
