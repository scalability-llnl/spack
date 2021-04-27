# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSpatstatData(RPackage):
    """Datasets for 'spatstat'

    Contains all the datasets for the 'spatstat' package."""

    homepage = "https://cloud.r-project.org/package=spatstat.data"
    url      = "https://cloud.r-project.org/src/contrib/spatstat.data_1.4-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatstat.data"

    version('1.7-0', sha256='bbc192d43f2b37b308566694cb48ecdbbc4f20ef44b6fc7636564a717a03c12f')
    version('1.4-3', sha256='8955b6ac40cc7d0d89e02334bb46f4c223ff0755e5818f132fee753e77918ea2')
    version('1.4-0', sha256='121e5bb92beb7ccac920f921e760f429fd71bcfe11cb9b07a7e7326c7a72ec8c')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.7-0:', type=('build', 'run'))
    depends_on('r-spatstat-utils', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
