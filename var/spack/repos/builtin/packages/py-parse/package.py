# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParse(PythonPackage):
    """parse() is the opposite of format()"""

    pypi = "parse/parse-1.11.1.tar.gz"

    license("MIT")

    version("1.18.0", sha256="91666032d6723dc5905248417ef0dc9e4c51df9526aaeef271eacad6491f06a4")
    version("1.12.1", sha256="a5fca7000c6588d77bc65c28f3f21bfce03b5e44daa8f9f07c17fe364990d717")
    version("1.11.1", sha256="870dd675c1ee8951db3e29b81ebe44fd131e3eb8c03a79483a58ea574f3145c2")

    depends_on("py-setuptools", type="build")
