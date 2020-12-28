# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBlis(PythonPackage):
    """Cython BLIS: Fast BLAS-like operations from Python and Cython,
    without the tears"""

    homepage = "https://github.com/explosion/cython-blis"
    url      = "https://pypi.io/packages/source/b/blis/blis-0.4.1.tar.gz"

    version('0.4.1', sha256='d69257d317e86f34a7f230a2fd1f021fd2a1b944137f40d8cdbb23bd334cd0c4')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.15:', type=('build', 'run'))
