# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeonames(RPackage):
    """geonames: Interface to the "Geonames" Spatial Query Web Service"""

    homepage = "https://cloud.r-project.org/package=geonames"
    url      = "https://cloud.r-project.org/src/contrib/geonames_0.999.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/geonames"

    version('0.999', sha256='1dd7bbd82d9425d14eb36f8e5bf431feaccfe3b0c4e70bf38f44f13dfc59e17b')

    depends_on('r@2.2.0:', type=('build', 'run'))
    depends_on('r-rjson', type=('build', 'run'))
