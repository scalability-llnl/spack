# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTraitsui(PythonPackage):
    """The TraitsUI project contains a toolkit-independent GUI abstraction
    layer, which is used to support the "visualization" features of the Traits
    package. Thus, you can write model in terms of the Traits API and specify a
    GUI in terms of the primitives supplied by TraitsUI (views, items, editors,
    etc.), and let TraitsUI and your selected toolkit and back-end take care of
    the details of displaying them."""

    homepage = "https://docs.enthought.com/traitsui"
    url      = "https://pypi.io/packages/source/t/traitsui/traitsui-6.1.3.tar.gz"

    version('6.1.3', sha256='48381763b181efc58eaf288431d1d92d028d0d97dfdd33eba7809aae8aef814f')

    variant('backend', default='pyqt5', description='Default backend',
            values=('wx', 'pyqt', 'pyqt5', 'pyside'), multi=False)

    depends_on('py-setuptools', type='build')
    depends_on('py-traits', type=('build', 'run'))
    depends_on('py-pyface@6.0.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Backends
    depends_on('py-wxpython@2.8.10:', when='backend=wx', type=('build', 'run'))
    depends_on('py-numpy', when='backend=wx', type=('build', 'run'))
    depends_on('py-pyqt4@4.10:', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pyqt5@5:', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pyside@1.2:', when='backend=pyside', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyside', type=('build', 'run'))
