# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConvevol(RPackage):
    """Quantifies and assesses the significance of convergent evolution"""

    homepage = "https://cloud.r-project.org/package=convevol"
    url      = "https://cloud.r-project.org/src/contrib/convevol_1.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/convevol/"

    version('1.3', sha256='d6b24b9796a559f5280e277746189d141151ade4b14cc6b4c2d9d496d7f314ac')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-geiger', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-phytools', type=('build', 'run'))
