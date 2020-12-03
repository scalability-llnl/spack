# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    url      = "https://pypi.io/packages/source/p/packaging/packaging-19.2.tar.gz"

    import_modules = ['packaging']

    version('19.2', sha256='28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47')
    version('19.1', sha256='c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe')
    version('19.0', sha256='0c98a5d0be38ed775798ece1b9727178c4469d9c3b4ada66e8e6b7849f8732af')
    version('17.1', sha256='f019b770dd64e585a99714f1fd5e01c7a8f11b45635aa953fd41c689a657375b')
    version('16.8', sha256='5d50835fdf0a7edf0b55e311b7c887786504efea1177abd7e69329a8e5ea619e')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('py-attrs', when='@19.1', type=('build', 'run'))
    depends_on('py-pyparsing@2.0.2:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Newer versions of setuptools require packaging. Although setuptools is an
    # optional dependency of packaging, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
