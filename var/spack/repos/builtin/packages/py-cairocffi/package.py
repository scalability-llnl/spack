# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCairocffi(PythonPackage):
    """cairocffi is a CFFI-based drop-in replacement for Pycairo, a set of
    Python bindings and object-oriented API for cairo. Cairo is a 2D vector
    graphics library with support for multiple backends including image
    buffers, PNG, PostScript, PDF, and SVG file output."""

    homepage = "https://github.com/Kozea/cairocffi"
    pypi = "cairocffi/cairocffi-1.0.2.tar.gz"

    version("1.0.2", sha256="01ac51ae12c4324ca5809ce270f9dd1b67f5166fe63bd3e497e9ea3ca91946ff")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@39.2.0:", type="build")
    depends_on("py-cffi@1.1.0:", type=("build", "run"))
