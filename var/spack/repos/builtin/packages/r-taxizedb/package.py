# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RTaxizedb(RPackage):
    """Tools for Working with 'Taxonomic' Databases

    Tools for working with 'taxonomic' databases, including utilities for
    downloading databases, loading them into various 'SQL' databases, cleaning
    up files, and providing a 'SQL' connection that can be used to do 'SQL'
    queries directly or used in 'dplyr'."""

    homepage = "https://cloud.r-project.org/package=taxizedb"
    url      = "https://cloud.r-project.org/src/contrib/taxizedb_0.1.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/taxizedb/"

    version('0.3.0', sha256='5f28338a233f0021097147e74c5f83107e5847de3413eceb308208e39af9fcb4')
    version('0.1.4', sha256='5a40569a2b5abe56201f112a10220150353412df39b7e8d21ea8698f424cf295')

    depends_on('r-curl@2.4:', type=('build', 'run'))
    depends_on('r-dbi@0.6-1:', type=('build', 'run'))
    depends_on('r-rsqlite@1.1.2:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-tibble', when='@0.3.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.3.0:', type=('build', 'run'))
    depends_on('r-readr@1.1.1:', when='@0.3.0:', type=('build', 'run'))
    depends_on('r-dbplyr@1.0.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-hoardr@0.1.0:', type=('build', 'run'))
    depends_on('r-rpostgresql@0.4.1:', when='@:0.1.4', type=('build', 'run'))
    depends_on('r-rmysql@0.10.11:', when='@:0.1.4', type=('build', 'run'))
