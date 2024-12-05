# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstpretty(PythonPackage):
    """Pretty print the output of python stdlib `ast.parse`."""

    homepage = "https://github.com/asottile/astpretty"
    pypi = "astpretty/astpretty-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="e4724bfd753636ba4a84384702e9796e5356969f40af2596d846ce64addde086")

    variant("typed", default=False, description="Add support for typed comments")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-typed-ast", type=("build", "run"), when="+typed")
