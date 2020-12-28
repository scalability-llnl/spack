# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgeos(RPackage):
    """Interface to Geometry Engine - Open Source ('GEOS') using the C
    'API' for topology operations on geometries. The 'GEOS' library is
    external to the package, and, when installing the package from source,
    must be correctly installed first. Windows and Mac Intel OS X binaries
    are provided on 'CRAN'."""

    homepage = "https://cloud.r-project.org/package=rgeos"
    url      = "https://cloud.r-project.org/src/contrib/rgeos_0.3-26.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgeos"

    version('0.5-1', sha256='8408973e7fe5648e39aa53f3d4bfe800638021a146a4e06f86496c0132e05488')
    version('0.3-26', sha256='98524a0b8113abe6c3d0ecc1f2f66e7ab6d40c783a76158cfc017e1ab1e3f433')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-sp@1.1-0:', type=('build', 'run'))
    depends_on('geos@3.2.0:3.8.0')
