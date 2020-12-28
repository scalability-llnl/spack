# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyMayavi(PythonPackage):
    """Mayavi: 3D visualization of scientific data in Python."""

    homepage = "https://docs.enthought.com/mayavi/mayavi/index.html"
    url      = "https://pypi.io/packages/source/m/mayavi/mayavi-4.7.1.tar.bz2"

    version('4.7.1', sha256='be51fb6f886f304f7c593c907e6a2e88d7919f8f446cdccfcd184fa35b3db724')

    depends_on('py-setuptools', type='build')
    depends_on('py-apptools', type=('build', 'run'))
    depends_on('py-envisage', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyface@6.1.1:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-traits@4.6.0:', type=('build', 'run'))
    depends_on('py-traitsui@6.0.0:', type=('build', 'run'))
    depends_on('vtk+python', type=('build', 'run'))
