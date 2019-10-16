# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymongo(PythonPackage):
    """The PyMongo distribution contains tools for interacting with
    MongoDB database from Python. The bson package is an implementation
    of the BSON format for Python. The pymongo package is a native
    Python driver for MongoDB. The gridfs package is a gridfs
    implementation on top of pymongo.

    PyMongo supports MongoDB 2.6, 3.0, 3.2, 3.4, 3.6, 4.0 and 4.2."""

    homepage = "https://pypi.org/project/pymongo/"
    url      = "https://pypi.io/packages/source/p/pymongo/pymongo-3.9.0.tar.gz"

    version('3.9.0', sha256='4249c6ba45587b959292a727532826c5032d59171f923f7f823788f413c2a5a3')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
