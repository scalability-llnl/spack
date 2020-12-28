# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBitarray(PythonPackage):
    """Efficient array of booleans - C extension"""

    homepage = "https://pypi.python.org/pypi/bitarray"
    url      = "https://pypi.io/packages/source/b/bitarray/bitarray-0.8.1.tar.gz"

    version('0.8.1', sha256='7da501356e48a83c61f479393681c1bc4b94e5a34ace7e08cb29e7dd9290ab18')

    depends_on('python')
    depends_on('py-setuptools', type='build')
