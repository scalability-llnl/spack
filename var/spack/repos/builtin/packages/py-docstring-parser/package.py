# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocstringParser(PythonPackage):
    """Parse Python docstrings in reST, Google and Numpydoc format."""

    homepage = "https://github.com/rr-/docstring_parser"
    pypi = "docstring-parser/docstring_parser-0.15.tar.gz"

    license("MIT")

    version("0.15", sha256="48ddc093e8b1865899956fcc03b03e66bb7240c310fac5af81814580c55bf682")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
