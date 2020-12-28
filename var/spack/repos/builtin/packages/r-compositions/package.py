# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCompositions(RPackage):
    """Compositional Data Analysis"""

    homepage = "https://cloud.r-project.org/package=compositions"
    url      = "https://cloud.r-project.org/src/contrib/compositions_1.40-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/compositions"

    version('1.40-2', sha256='110d71ae000561987cb73fc76cd953bd69d37562cb401ed3c36dca137d01b78a')

    depends_on('r@2.2.0:', type=('build', 'run'))
    depends_on('r-tensora', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-energy', type=('build', 'run'))
    depends_on('r-bayesm', type=('build', 'run'))
