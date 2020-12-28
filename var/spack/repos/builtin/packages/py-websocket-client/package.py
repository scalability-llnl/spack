# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyWebsocketClient(PythonPackage):
    """WebSocket client for Python. hybi13 is supported."""

    homepage = "https://github.com/websocket-client/websocket-client.git"
    url      = "https://pypi.io/packages/source/w/websocket_client/websocket_client-0.57.0.tar.gz"

    version('0.57.0', sha256='d735b91d6d1692a6a181f2a8c9e0238e5f6373356f561bb9dc4c7af36f452010')
    version('0.56.0', sha256='1fd5520878b68b84b5748bb30e592b10d0a91529d5383f74f4964e72b297fd3a')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname', when='^python@2.6:2.7.9', type=('build', 'run'))
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
