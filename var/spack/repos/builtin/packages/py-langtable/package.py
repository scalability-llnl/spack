# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLangtable(PythonPackage):
    """Python module to query the langtable-data."""

    homepage = "https://github.com/mike-fabian/langtable"
    url      = "https://github.com/mike-fabian/langtable/releases/download/0.0.53/langtable-0.0.53.tar.gz"

    version('0.0.53', sha256='fb17fd4d8e491c79159f81aa06ebacb18673fce59dac96f4e9d2d2db27a2e374')
    version('0.0.52', sha256='b40bbd38a4afa536ba139db12eb1f59a257153a839f08cb459b89256fdc417c8')
    version('0.0.51', sha256='8d4615cc0bb0fa49faa05b55ff49b1f41122b8092ca18a5d10f1e1699d6d7b3c')

    depends_on('py-setuptools', type='build')
