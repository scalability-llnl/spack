# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RViridislite(RPackage):
    """viridisLite: Default Color Maps from 'matplotlib' (Lite Version)"""

    homepage = "https://github.com/sjmgarnier/viridisLite"
    url      = "https://cloud.r-project.org/src/contrib/viridisLite_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/viridisLite"

    version('0.3.0', sha256='780ea12e7c4024d5ba9029f3a107321c74b8d6d9165262f6e64b79e00aa0c2af')
    version('0.2.0', '04a04415cf651a2b5f964b261896c0fb')

    depends_on('r@2.1.0:', type=('build', 'run'))
