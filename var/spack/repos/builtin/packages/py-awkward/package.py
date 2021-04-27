# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAwkward(PythonPackage):
    """Manipulate JSON-like data with NumPy-like idioms."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    pypi = "awkward/awkward-1.1.2.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers = ['vvolkl']

    version('1.2.2', sha256='89f126a072d3a6eee091e1afeed87e0b2ed3c34ed31a1814062174de3cab8d9b')
    version('1.1.2', sha256='4ae8371d9e6d5bd3e90f3686b433cebc0541c88072655d2c75ec58e79b5d6943')

    patch('pybind11.patch')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.13.1:', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'link'))
    depends_on('dlpack', when="@1.0.0:")
    depends_on('rapidjson')
    depends_on('cmake', type='build')
