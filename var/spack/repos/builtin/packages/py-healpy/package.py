# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHealpy(PythonPackage):
    """healpy is a Python package to handle pixelated data on the sphere."""

    homepage = "https://healpy.readthedocs.io/"
    url      = "https://pypi.python.org/packages/source/h/healpy/healpy-1.13.0.tar.gz"

    version('1.13.0', sha256='d0ae02791c2404002a09c643e9e50bc58e3d258f702c736dc1f39ce1e6526f73')
    version('1.7.4', sha256='3cca7ed7786ffcca70e2f39f58844667ffb8521180ac890d4da651b459f51442')

    depends_on('python', type=('build', 'run'))
    depends_on('py-setuptools@3.2:', type='build')
    depends_on('py-numpy@1.13:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
