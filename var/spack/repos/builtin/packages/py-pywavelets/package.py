# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPywavelets(PythonPackage):
    """PyWavelets is a free Open Source library for wavelet transforms
       in Python"""

    homepage = "https://github.com/PyWavelets"
    url = "https://pypi.io/packages/source/P/PyWavelets/PyWavelets-0.5.2.tar.gz"

    version('1.1.1', sha256='1a64b40f6acb4ffbaccce0545d7fc641744f95351f62e4c6aaa40549326008c9')
    version('0.5.2', sha256='ce36e2f0648ea1781490b09515363f1f64446b0eac524603e5db5e180113bed9')

    depends_on('python@3.5:', type=('build', 'run'), when='@1.1.1:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.9.1:',  type=('build', 'run'))
    depends_on('py-numpy@1.13.3:',  type=('build', 'run'), when='@1.1.1:')
