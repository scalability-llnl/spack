# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpydoc(PythonPackage):
    """numpydoc - Numpy's Sphinx extensions"""

    homepage = "https://github.com/numpy/numpydoc"
    url      = "https://pypi.io/packages/source/n/numpydoc/numpydoc-0.6.0.tar.gz"

    version('0.6.0', sha256='1ec573e91f6d868a9940d90a6599f3e834a2d6c064030fbe078d922ee21dcfa1')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-sphinx@1.0.1:', type='build')
