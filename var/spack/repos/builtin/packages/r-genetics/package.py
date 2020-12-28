# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenetics(RPackage):
    """genetics: Population Genetics"""

    homepage = "https://cloud.r-project.org/package=genetics"
    url      = "https://cloud.r-project.org/src/contrib/genetics_1.3.8.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/genetics"

    version('1.3.8.1.2', sha256='30cb67de2e901578fd802deb7fbfea6c93024c9fb6ea66cad88430a3a2a51eec')

    depends_on('r-combinat', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
