# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPly(PythonPackage):
    """Python Lex & Yacc."""

    homepage = "http://www.dabeaz.com/ply"
    pypi = "ply/ply-3.11.tar.gz"

    license("Unlicense")

    version("3.11", sha256="00c7c1aaa88358b9c765b6d3000c6eec0ba42abca5351b095321aef446081da3")
    version("3.8", sha256="e7d1bdff026beb159c9942f7a17e102c375638d9478a7ecd4cc0c76afd8de0b8")

    depends_on("py-setuptools", type="build")
