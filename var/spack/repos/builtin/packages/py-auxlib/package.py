# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAuxlib(PythonPackage):
    """Auxlib is an auxiliary library to the python standard library."""

    homepage = "https://github.com/kalefranz/auxlib"
    url      = "https://pypi.io/packages/source/a/auxlib/auxlib-0.0.43.tar.gz"

    version('0.0.43', sha256='0f175637e96a090a785767ce28483cf1aeec316a19afce9b2fbd113e1122786a')

    depends_on('py-setuptools', type='build')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')
    depends_on('py-ordereddict', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-wheel', type=('build', 'run'))
