# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatial(RPackage):
    """spatial: Functions for Kriging and Point Pattern Analysis"""

    homepage = "https://cloud.r-project.org/package=spatial"
    url      = "https://cloud.r-project.org/src/contrib/spatial_7.3-11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatial"

    version('7.3-11', sha256='624448d2ac22e1798097d09fc5dc4605908a33f490b8ec971fc6ea318a445c11')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
