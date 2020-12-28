# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAwkward1(PythonPackage):
    """ROOT I/O in pure Python and NumPy."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    url = "https://github.com/scikit-hep/awkward-1.0/archive/0.3.1.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers = ['vvolkl']

    version('0.3.1', sha256='7126d9feab8828b0b4f4c6dbc9e28c269a91e28eef4a6033d7ebb5db21f1dab3')

    patch('pybind11.patch')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.13.1:')
    depends_on('py-pybind11')
    depends_on('rapidjson')
    depends_on('cmake', type='build')
