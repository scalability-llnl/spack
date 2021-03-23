# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAwkward1(PythonPackage):
    """DEPRECATED! This package was renamed to py-awkward."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    url = "https://github.com/scikit-hep/awkward-1.0/archive/0.3.1.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers = ['vvolkl']

    version('1.1.2', sha256='626e3a6a2a92dd67abc8692b1ebfa1b447b9594352d6ce8c86c37d7299dc4602', deprecated=True)
    version('0.3.1', sha256='7126d9feab8828b0b4f4c6dbc9e28c269a91e28eef4a6033d7ebb5db21f1dab3', deprecated=True)

    patch('pybind11.patch')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.13.1:', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'link'))
    depends_on('dlpack', when="@1.0.0:")
    depends_on('rapidjson')
    depends_on('cmake', type='build')
