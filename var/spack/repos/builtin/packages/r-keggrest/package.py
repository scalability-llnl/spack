# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKeggrest(RPackage):
    """Client-side REST access to KEGG.

       A package that provides a client interface to the KEGG REST server.
       Based on KEGGSOAP by J. Zhang, R. Gentleman, and Marc Carlson, and KEGG
       (python package) by Aurelien Mazurie."""

    homepage = "https://bioconductor.org/packages/KEGGREST"
    git      = "https://git.bioconductor.org/packages/KEGGREST.git"

    version('1.24.1', commit='bbc3ef476e02147aad8e1f33178136cc797c1b3f')
    version('1.22.0', commit='4374507376be811d29416d0cbbfd9115a50494d9')
    version('1.20.2', commit='62b4519367841f3548536c117e7e2bfe3fa4bf72')
    version('1.18.1', commit='580c126eabc3c52145967708f67a428ca46b23b2')
    version('1.16.1', commit='ed48de0def57a909894e237fa4731c4a052d8849')

    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
