# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPyface(PythonPackage):
    """The pyface project contains a toolkit-independent GUI abstraction layer,
    which is used to support the "visualization" features of the Traits
    package. Thus, you can write code in terms of the Traits API (views, items,
    editors, etc.), and let pyface and your selected toolkit and back-end take
    care of the details of displaying them."""

    homepage = "https://docs.enthought.com/pyface"
    url      = "https://pypi.io/packages/source/p/pyface/pyface-6.1.2.tar.gz"

    version('6.1.2', sha256='7c2ac3d5cbec85e8504b3b0b63e9307be12c6d710b46bae372ce6562d41f4fbc')

    variant('backend', default='pyqt5', description='Default backend',
            values=('wx', 'pyqt', 'pyqt5', 'pyside'), multi=False)

    depends_on('py-setuptools', type='build')
    depends_on('py-traits', type=('build', 'run'))

    # Backends
    depends_on('py-wxpython@2.8.10:', when='backend=wx', type=('build', 'run'))
    depends_on('py-numpy', when='backend=wx', type=('build', 'run'))
    depends_on('py-pyqt4@4.10:', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pyqt5@5:', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pyside@1.2:', when='backend=pyside', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyside', type=('build', 'run'))
