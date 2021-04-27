# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPygeos(PythonPackage):
    """PyGEOS is a C/Python library with vectorized geometry functions.

    The geometry operations are done in the open-source geometry library GEOS.
    PyGEOS wraps these operations in NumPy ufuncs providing a performance
    improvement when operating on arrays of geometries."""

    homepage = "https://github.com/pygeos/pygeos"
    pypi = "pygeos/pygeos-0.8.tar.gz"

    maintainers = ['adamjstewart']

    version('0.9', sha256='c0584b20e95f80ee57277a6eb1e5d7f86600f8b1ef3c627d238e243afdcc0cc7')
    version('0.8', sha256='45b7e1aaa5fc9ff53565ef089fb75c53c419ace8cee18385ec1d7c1515c17cbc')

    depends_on('python@3:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.13:', when='@0.9:', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.10:', type=('build', 'link', 'run'))
    depends_on('geos@3.5:')
