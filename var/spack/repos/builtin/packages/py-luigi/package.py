# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLuigi(PythonPackage):
    """Workflow mgmgt + task scheduling + dependency resolution"""

    homepage = "https://github.com/spotify/luigi"
    url      = "https://pypi.io/packages/source/l/luigi/luigi-2.8.3.tar.gz"

    version('2.8.3', sha256='8b5c84a3c3f4df07309056d3b98348b93c054f1931b7ee22fc29e7989f645c9e')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-tornado@4.0:4.99', type=('build', 'run'))
    depends_on('py-python-daemon@:2.1', type=('build', 'run'))
    depends_on('py-python-dateutil@2.7.5', when='@2.8.3:', type=('build', 'run'))
