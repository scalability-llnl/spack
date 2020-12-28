# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypyExtensions(PythonPackage):
    """Experimental type system extensions for programs checked with the
    mypy typechecker."""

    homepage = "https://github.com/python/mypy_extensions"
    url      = "https://pypi.io/packages/source/m/mypy-extensions/mypy_extensions-0.4.3.tar.gz"

    version('0.4.3', sha256='2d82818f5bb3e369420cb3c4060a7970edba416647068eb4c5343488a6c604a8')

    depends_on('py-setuptools', type='build')
    depends_on('py-typing@3.5.3:', when='^python@:3.4', type=('build', 'run'))
