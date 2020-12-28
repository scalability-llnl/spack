# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRUtils(RPackage):
    """Utility functions useful when programming and
    developing R packages."""

    homepage = "https://github.com/HenrikBengtsson/R.utils"
    url      = "https://cloud.r-project.org/src/contrib/R.utils_2.5.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/R.utils"

    version('2.9.0', sha256='b2aacc5a55d3ea86c41ac576d2583e446af145f4cb1103ad7b6f95b09ab09ff0')
    version('2.5.0', sha256='1ae1a0f0c6a4972bb2369a2dbccd29ade87d747255ff9cb5a0bd784a5be1039f')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-r-oo@1.22.0:', type=('build', 'run'))
    depends_on('r-r-methodss3@1.7.1:', type=('build', 'run'))
