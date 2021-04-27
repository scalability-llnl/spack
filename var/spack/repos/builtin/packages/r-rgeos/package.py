# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRgeos(RPackage):
    """Interface to Geometry Engine - Open Source ('GEOS')

    Interface to Geometry Engine - Open Source ('GEOS') using the C 'API' for
    topology operations on geometries. The 'GEOS' library is external to the
    package, and, when installing the package from source, must be correctly
    installed first. Windows and Mac Intel OS X binaries are provided on
    'CRAN'. ('rgeos' >= 0.5-1): Up to and including 'GEOS' 3.7.1, topological
    operations succeeded with some invalid geometries for which the same
    operations fail from and including 'GEOS' 3.7.2. The 'checkValidity='
    argument defaults and structure have been changed, from default FALSE to
    integer default '0L' for 'GEOS' < 3.7.2 (no check), '1L' 'GEOS' >= 3.7.2
    (check and warn). A value of '2L' is also provided that may be used,
    assigned globally using 'set_RGEOS_CheckValidity(2L)', or locally using the
    'checkValidity=2L' argument, to attempt zero-width buffer repair if invalid
    geometries are found. The previous default (FALSE, now '0L') is fastest and
    used for 'GEOS' < 3.7.2, but will not warn users of possible problems
    before the failure of topological operations that previously succeeded.
    From 'GEOS' 3.8.0, repair of geometries may also be attempted using
    'gMakeValid()', which may, however, return a collection of geometries of
    different types."""

    homepage = "https://cloud.r-project.org/package=rgeos"
    url      = "https://cloud.r-project.org/src/contrib/rgeos_0.3-26.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgeos"

    version('0.5-5', sha256='4baa0dfe6ff76e87ddb67a030fc14fe963d28b518485a4d71058923b2606d420')
    version('0.5-1', sha256='8408973e7fe5648e39aa53f3d4bfe800638021a146a4e06f86496c0132e05488')
    version('0.3-26', sha256='98524a0b8113abe6c3d0ecc1f2f66e7ab6d40c783a76158cfc017e1ab1e3f433')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-sp@1.1-0:', type=('build', 'run'))
    depends_on('geos@3.2.0:3.8.0')
