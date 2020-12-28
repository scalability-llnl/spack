# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocfilecache(RPackage):
    """Manage Files Across Sessions.

       This package creates a persistent on-disk cache of files that the user
       can add, update, and retrieve. It is useful for managing resources (such
       as custom Txdb objects) that are costly or difficult to create, web
       resources, and data files used across sessions."""

    homepage = "https://bioconductor.org/packages/BiocFileCache"
    git      = "https://git.bioconductor.org/packages/BiocFileCache.git"

    version('1.8.0', commit='0e3542b6aae849b01240d8055a48da1b267bd5a0')
    version('1.6.0', commit='c2de6c1cdef6294e5d0adea31e4ebf25865742ba')
    version('1.4.0', commit='a2c473d17f78899c7899b9638faea8c30735eb80')
    version('1.2.3', commit='d78bf5b46c8a329f5ddef879fe51230444bc42f8')
    version('1.0.1', commit='dbf4e8dd4d8d9f475066cd033481efe95c56df75')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-dbplyr@1.0.0:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))

    depends_on('r-curl', when='@1.6.0:', type=('build', 'run'))
