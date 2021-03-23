# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLwgeom(RPackage):
    """Bindings to Selected 'liblwgeom' Functions for Simple Features

    Access to selected functions found in 'liblwgeom'
    <https://github.com/postgis/postgis/tree/master/liblwgeom>, the
    light-weight geometry library used by 'PostGIS' <http://postgis.net/>."""

    homepage = "https://github.com/r-spatial/lwgeom/"
    cran     = "lwgeom"

    version('0.2-5', sha256='4a1d93f96c10c2aac173d8186cf7d7bef7febcb3cf066a7f45da32251496d02f')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-units', type=('build', 'run'))
    depends_on('r-sf@0.9-3:', type=('build', 'run'))
    depends_on('geos@3.5.0:')
    depends_on('proj@4.8.0:6.999')
