# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNimble(AutotoolsPackage):
    """A system for writing hierarchical statistical models largely
       compatible with 'BUGS' and 'JAGS', writing nimbleFunctions to
       operate models and do basic R-style math, and compiling both
       models and nimbleFunctions via custom- generated C++.
    """

    homepage = "https://cloud.r-project.org/package=nimble"
    url      = "https://cloud.r-project.org/src/contrib/nimble_0.9.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nimble"

    version('0.9.1', sha256='ad5e8a171193cb0172e68bf61c4f94432c45c131a150101ad1c5c7318c335757')
    version('0.9.0', sha256='ebc28fadf933143eea73900cacaf96ff81cb3c2d607405016062b7e93afa5611')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('automake')
