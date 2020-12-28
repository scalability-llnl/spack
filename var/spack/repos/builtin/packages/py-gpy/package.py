# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGpy(PythonPackage):
    """The Gaussian Process Toolbox."""

    homepage = "http://sheffieldml.github.com/GPy/"
    url      = "https://pypi.io/packages/source/g/gpy/GPy-1.9.9.tar.gz"

    version('1.9.9', sha256='04faf0c24eacc4dea60727c50a48a07ddf9b5751a3b73c382105e2a31657c7ed')
    version('0.8.8', sha256='e135d928cf170e2ec7fb058a035b5a7e334dc6b84d0bfb981556782528341988')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-scipy@0.16:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-paramz@0.9.0:', type=('build', 'run'))
    depends_on('py-cython@0.29:', type='build')
