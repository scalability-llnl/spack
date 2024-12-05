# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEpydoc(PythonPackage):
    """Epydoc is a tool for generating API documentation documentation for
    Python modules, based on their docstrings."""

    pypi = "epydoc/epydoc-3.0.1.tar.gz"

    license("MIT")

    version("3.0.1", sha256="c81469b853fab06ec42b39e35dd7cccbe9938dfddef324683d89c1e5176e48f2")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
