# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRbgl(RPackage):
    """An interface to the BOOST graph library.

       A fairly extensive and comprehensive interface to the graph algorithms
       contained in the BOOST library."""

    homepage = "https://bioconductor.org/packages/RBGL"
    git      = "https://git.bioconductor.org/packages/RBGL.git"

    version('1.60.0', commit='ef24c17c411659b8f030602bd9781c534d6ec93b')
    version('1.58.2', commit='086ad0c6bab7be29311b6ae14fd39df7a21331a6')
    version('1.56.0', commit='a1fa9d89c6a3401892c5dd1493df6a14031f0912')
    version('1.54.0', commit='e9c743d380e83c155495cb8732102f01f213c905')
    version('1.52.0', commit='93e8fcfafec8f1cd5638fe30dc0f9506d15b49c0')

    depends_on('r-graph', type=('build', 'run'))

    depends_on('r-bh', when='@1.60.0:', type=('build', 'run'))
