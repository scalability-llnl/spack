# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNuitka(PythonPackage):
    """Nuitka is the Python compiler. It is written in Python. It is a
    seamless replacement or extension to the Python interpreter and
    compiles every construct that Python has, when itself run with that
    Python version."""

    homepage = "https://nuitka.net/"
    pypi = "Nuitka/Nuitka-2.2.1.tar.gz"
    git = "https://github.com/Nuitka/Nuitka.git"

    license("Apache-2.0")

    version("2.2.1", sha256="7bf67e80f94c93017fbaacfe1e277b92422d234a3c849a1555e43848f5fb27a1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-ordered-set", type="build")
