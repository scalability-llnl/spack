# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysocks(PythonPackage):
    """A Python SOCKS client module."""

    homepage = "https://github.com/Anorov/PySocks"
    pypi = "PySocks/PySocks-1.7.1.tar.gz"

    license("BSD-3-Clause")

    version("1.7.1", sha256="3f8804571ebe159c380ac6de37643bb4685970655d3bba243530d6558b799aa0")
    version("1.6.6", sha256="02419a225ff5dcfc3c9695ef8fc9b4d8cc99658e650c6d4718d4c8f451e63f41")
    version("1.5.7", sha256="e51c7694b10288e6fd9a28e15c0bcce9aca0327e7b32ebcd9af05fcd56f38b88")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
