# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyImmutables(PythonPackage):
    """An immutable mapping type for Python."""

    homepage = "https://github.com/MagicStack/immutables"
    url      = "https://pypi.io/packages/source/i/immutables/immutables-0.14.tar.gz"

    version('0.14', sha256='a0a1cc238b678455145bae291d8426f732f5255537ed6a5b7645949704c70a78')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
