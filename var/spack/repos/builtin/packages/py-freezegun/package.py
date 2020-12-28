# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFreezegun(PythonPackage):
    """FreezeGun is a library that allows your Python tests to travel
    through time by mocking the datetime module."""

    homepage = "https://github.com/spulec/freezegun"
    url      = "https://pypi.io/packages/source/f/freezegun/freezegun-0.3.12.tar.gz"

    version('0.3.12', sha256='2a4d9c8cd3c04a201e20c313caf8b6338f1cfa4cda43f46a94cc4a9fd13ea5e7')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-python-dateutil@1.0:1.999', type=('build', 'run'), when='^python@:2')
    depends_on('py-python-dateutil@2:', type=('build', 'run'), when='^python@3:')
