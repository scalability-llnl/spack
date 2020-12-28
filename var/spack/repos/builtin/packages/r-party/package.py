# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParty(RPackage):
    """A computational toolbox for recursive partitioning."""

    homepage = "https://cloud.r-project.org/package=party"
    url      = "https://cloud.r-project.org/src/contrib/party_1.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/party"

    version('1.3-3', sha256='9f72eea02d43a4cee105790ae7185b0478deb6011ab049cc9d31a0df3abf7ce9')
    version('1.3-2', sha256='9f350fa21114151c49bccc3d5f8536dbc5a608cfd88f60461c9805a4c630510b')
    version('1.1-2', sha256='c3632b4b02dc12ec949e2ee5b24004e4a4768b0bc9737432e9a85acbc2ed0e74')

    depends_on('r@2.14.0:', when='@:1.2-2', type=('build', 'run'))
    depends_on('r@3.0.0:', when='@1.2-3:', type=('build', 'run'))
    depends_on('r-mvtnorm@1.0-2:', type=('build', 'run'))
    depends_on('r-modeltools@0.2-21:', type=('build', 'run'))
    depends_on('r-strucchange', type=('build', 'run'))
    depends_on('r-survival@2.37-7:', type=('build', 'run'))
    depends_on('r-coin@1.1-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-sandwich@1.1-1:', type=('build', 'run'))
