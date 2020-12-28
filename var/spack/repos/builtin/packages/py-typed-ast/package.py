# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypedAst(PythonPackage):
    """A fork of Python 2 and 3 ast modules with type comment support."""

    homepage = "https://github.com/python/typed_ast"
    url      = "https://pypi.io/packages/source/t/typed-ast/typed_ast-1.4.0.tar.gz"

    version('1.4.0', sha256='66480f95b8167c9c5c5c87f32cf437d585937970f3fc24386f313a4c97b44e34')

    depends_on('python@3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
