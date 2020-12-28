# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatUtils(RPackage):
    """Contains utility functions for the 'spatstat'
       package which may also be useful for other purposes.
    """

    homepage = "https://cloud.r-project.org/package=spatstat.utils"
    url      = "https://cloud.r-project.org/src/contrib/spatstat.utils_1.17-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatstat.utils"

    version('1.17-0', sha256='39cd683ed7f41d8adc9e28af073d91b244aa1cf5ad966dfbb396ee3ee79f0922')
    version('1.15-0', sha256='90e07d730b6939f47f93c939afae10874b2c82bd402960ede4133de67dca2a0c')

    depends_on('r@3.3.0:', type=('build', 'run'))
