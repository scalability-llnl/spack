# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPortalocker(PythonPackage):
    """Portalocker is a library to provide an easy API to file
    locking."""

    homepage = "https://github.com/WoLpH/portalocker"
    url      = "https://github.com/WoLpH/portalocker/archive/v1.6.0.tar.gz"

    version('1.6.0', sha256='084ff315ccb9fb38a7c06155d409da5df29647da7c6d2bc2b24637f9f79001ff')

    depends_on('py-setuptools@38.3.0:', type='build')
