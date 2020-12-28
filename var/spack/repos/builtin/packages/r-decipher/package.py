# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDecipher(RPackage):
    """Tools for curating, analyzing, and manipulating biological sequences."""

    homepage = "https://bioconductor.org/packages/DECIPHER"
    git      = "https://git.bioconductor.org/packages/DECIPHER.git"

    version('2.12.0', commit='658ae23870383b25b96a03a18d4ecac228a2650f')
    version('2.10.2', commit='db7b017c9050a7ec1d4daa15352994890095e9c3')
    version('2.8.1', commit='35aa66f48e06b93a98d1060c90c44d34ce05ccd9')
    version('2.6.0', commit='ed9acaa35c8774cb0ea01cd7cc2e46d063d8c70e')
    version('2.4.0', commit='1a57b8e4c7d7dec1c233f79c9a88d3705e0ad432')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-biostrings@2.35.12:', type=('build', 'run'))
    depends_on('r-rsqlite@1.1:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
