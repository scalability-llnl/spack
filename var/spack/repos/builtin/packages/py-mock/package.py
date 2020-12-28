# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMock(PythonPackage):
    """mock is a library for testing in Python. It allows you to replace parts
    of your system under test with mock objects and make assertions about how
    they have been used."""

    homepage = "https://github.com/testing-cabal/mock"
    url      = "https://pypi.io/packages/source/m/mock/mock-3.0.5.tar.gz"

    version('3.0.5', sha256='83657d894c90d5681d62155c82bda9c1187827525880eda8ff5df4ec813437c3')
    version('2.0.0', sha256='b158b6df76edd239b8208d481dc46b6afd45a846b7812ff0ce58971cf5bc8bba')
    version('1.3.0', sha256='1e247dbecc6ce057299eb7ee019ad68314bb93152e81d9a6110d35f4d5eca0f6')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.7:', type=('build', 'run'))
    depends_on('py-six@1.9:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-funcsigs@1:', type=('build', 'run'), when='^python@:3.2')
