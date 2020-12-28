# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTaxizedb(RPackage):
    """taxizedb: Tools for Working with 'Taxonomic' Databases"""

    homepage = "https://cloud.r-project.org/package=taxizedb"
    url      = "https://cloud.r-project.org/src/contrib/taxizedb_0.1.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/taxizedb/"

    version('0.1.4', sha256='5a40569a2b5abe56201f112a10220150353412df39b7e8d21ea8698f424cf295')

    depends_on('r-curl@2.4:', type=('build', 'run'))
    depends_on('r-dbi@0.6-1:', type=('build', 'run'))
    depends_on('r-rpostgresql@0.4.1:', type=('build', 'run'))
    depends_on('r-rmysql@0.10.11:', type=('build', 'run'))
    depends_on('r-rsqlite@1.1.2:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-dbplyr@1.0.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-hoardr@0.1.0:', type=('build', 'run'))
