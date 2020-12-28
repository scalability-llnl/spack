# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXmapbridge(RPackage):
    """Export plotting files to the xmapBridge for visualisation in X:Map.

       xmapBridge can plot graphs in the X:Map genome browser. This package
       exports plotting files in a suitable format."""

    homepage = "https://bioconductor.org/packages/xmapbridge"
    git      = "https://git.bioconductor.org/packages/xmapbridge.git"

    version('1.42.0', commit='d79c80dfc1a0ed3fd6d3e7a7c3a4aff778537ca9')
    version('1.40.0', commit='00a2993863f28711e237bc937fa0ba2d05f81684')
    version('1.38.0', commit='08138f00385fa0c669ff4cc33d7eac3d29cd615d')
    version('1.36.0', commit='e44f648c9da9eaa130849a738d90dc11685050e2')
    version('1.34.0', commit='f162e1f72ead5f5a1aede69032d5771a6572d965')

    depends_on('r@2.0:', type=('build', 'run'))
