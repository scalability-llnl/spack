# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFnPy(PythonPackage):
    """Functional programming in Python: implementation of missing features
    to enjoy FP."""

    homepage = "https://github.com/fnpy/fn.py"
    url = "https://github.com/fnpy/fn.py/archive/v0.5.2.tar.gz"

    license("Apache-2.0")

    version("0.6.0", sha256="85d4d4ae6ce3c13e9dbe45df2895188f742ebddbf100a95d360d73a8965ee0c8")
    version("0.5.2", sha256="fda2253d792867a79514496932630622df9340f214a2f4b2d597b60a8cc3d96b")

    depends_on("py-setuptools", type="build")

    # Uses inspect.getargspec
    depends_on("python@:3.10", when="@:0.5", type=("run", "build"))
