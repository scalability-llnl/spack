# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypyExtensions(PythonPackage):
    """Experimental type system extensions for programs checked with the
    mypy typechecker."""

    homepage = "https://github.com/python/mypy_extensions"
    pypi = "mypy-extensions/mypy_extensions-0.4.3.tar.gz"

    license("MIT")

    version("1.0.0", sha256="75dbf8955dc00442a438fc4d0666508a9a97b6bd41aa2f0ffe9d2f2725af0782")
    version("0.4.3", sha256="2d82818f5bb3e369420cb3c4060a7970edba416647068eb4c5343488a6c604a8")

    depends_on("py-setuptools", type="build")
