# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlssDist(RPackage):
    """gamlss.dist: Distributions for Generalized Additive Models for
       Location Scale and Shape"""

    homepage = "https://cloud.r-project.org/package=gamlss.dist"
    url      = "https://cloud.r-project.org/src/contrib/gamlss.dist_5.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gamlss.dist/"

    version('5.1-4', sha256='343c6ca0fd8a1c1dfdf9ffc65c95d4dae0c6c80b3e60fccba003e5171f3d287e')
    version('5.1-3', sha256='87fd643c82579519b67c66c1d87383fa1e203e8b09f607649ee7bce142bda404')
    version('5.1-1', sha256='44f999ff74ee516757eb39c8308c48aa850523aad2f38e622268313a13dda0b1')

    depends_on('r@2.15:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
