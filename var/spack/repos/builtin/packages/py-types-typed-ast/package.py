# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesTypedAst(PythonPackage):
    """Typing stubs for typed-ast."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-typed-ast/types-typed-ast-1.5.8.3.tar.gz"

    version("1.5.8.7", sha256="f7795f6f9d597b35212314040b993f6613b51d81738edce3c1e3a3e9ef655124")
    version("1.5.8.3", sha256="3a62bc25168f8b44ce74e1114f9fbc2ee87d6e96e3880cbef39aad9522555b4e")

    depends_on("py-setuptools", type="build")
