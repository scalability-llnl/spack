# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyDocker(PythonPackage):
    """A Python library for the Docker Engine API."""

    homepage = "https://github.com/docker/docker-py"
    url      = "https://pypi.io/packages/source/d/docker/docker-4.2.1.tar.gz"

    version('4.2.1', sha256='380a20d38fbfaa872e96ee4d0d23ad9beb0f9ed57ff1c30653cbeb0c9c0964f2')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.4.0:', type=('build', 'run'))
    depends_on('py-websocket-client@0.32.0:', type=('build', 'run'))
    depends_on('py-requests@2.14.2:2.17.999,2.18.1:', type=('build', 'run'))
    depends_on('py-backports-ssl-match-hostname@3.5:', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-ipaddress@1.0.16:', when='^python@:3.2', type=('build', 'run'))
