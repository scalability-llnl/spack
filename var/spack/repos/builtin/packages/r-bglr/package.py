# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBglr(RPackage):
    """BGLR: Bayesian Generalized Linear Regression"""

    homepage = "https://cloud.r-project.org/package=BGLR"
    url      = "https://cloud.r-project.org/src/contrib/BGLR_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/BGLR"

    version('1.0.8', sha256='5e969590d80b2f272c02a43b487ab1ffa13af386e0342993e6ac484fc82c9b95')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-truncnorm', type=('build', 'run'))
