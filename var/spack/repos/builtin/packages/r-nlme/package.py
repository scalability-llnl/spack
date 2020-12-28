# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNlme(RPackage):
    """Fit and compare Gaussian linear and nonlinear mixed-effects models."""

    homepage = "https://cloud.r-project.org/package=nlme"
    url      = "https://cloud.r-project.org/src/contrib/nlme_3.1-130.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nlme"

    version('3.1-141', sha256='910046260a03d8f776ac7b0766b5adee91556829d0d8a70165b2c695ce038056')
    version('3.1-139', sha256='0460fc69d85122177e7ef01bad665d56bcaf63d31bdbfdbdfdcba2c082085739')
    version('3.1-131', sha256='79daa167eb9bc7d8dba506da4b24b5250665b051d4e0a51dfccbb0087fdb564c')
    version('3.1-130', sha256='ec576bd906ef2e1c79b6a4382743d425846f63be2a43de1cce6aa397b40e290e')

    depends_on('r@3.0.2:', when='@:3.1-131', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@3.1-131.1', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@3.1-135.5:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@3.1-134:3.1-135', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
