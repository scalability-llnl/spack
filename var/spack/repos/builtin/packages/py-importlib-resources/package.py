# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibResources(PythonPackage):
    """Read resources from Python packages"""

    homepage = "https://pypi.org/project/importlib_resources/"
    url      = "https://pypi.io/packages/source/i/importlib_resources/importlib_resources-1.0.2.tar.gz"

    version('1.0.2', sha256='d3279fd0f6f847cced9f7acc19bd3e5df54d34f93a2e7bb5f238f81545787078')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-pathlib2', when='^python@:2', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
