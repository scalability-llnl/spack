# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpydoc(PythonPackage):
    """numpydoc - Numpy's Sphinx extensions"""

    homepage = "https://github.com/numpy/numpydoc"
    pypi = "numpydoc/numpydoc-0.6.0.tar.gz"

    version('1.1.0', sha256='c36fd6cb7ffdc9b4e165a43f67bf6271a7b024d0bb6b00ac468c9e2bfc76448e')
    version('0.6.0', sha256='1ec573e91f6d868a9940d90a6599f3e834a2d6c064030fbe078d922ee21dcfa1')

    depends_on('python@2.6:2.8,3.3:', when='@0.6.0')
    depends_on('python@3.5:', when='@1.1.0')
    depends_on('py-setuptools',    type='build')
    depends_on('py-sphinx@1.0.1:1.6.7', type='build', when='@0.6.0')
    depends_on('py-sphinx@1.6.5:', type='build', when='@1.1.0')
    depends_on('py-jinja2@2.3:', type='build', when='@1.1.0')
