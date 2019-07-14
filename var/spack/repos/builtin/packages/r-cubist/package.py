# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCubist(RPackage):
    """Regression modeling using rules with added instance-based corrections"""

    homepage = "https://cran.r-project.org/package=Cubist"
    url      = "https://cran.r-project.org/src/contrib/Cubist_0.0.19.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Cubist"

    version('0.2.1', sha256='b310c3f166f15fa3e16f8d110d39931b0bb1b0aa8d0c9ac2af5a9a45081588a3')
    version('0.0.19', 'bf9364f655536ec03717fd2ad6223a47')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
