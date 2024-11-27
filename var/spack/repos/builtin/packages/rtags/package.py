# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rtags(CMakePackage):
    """RTags is a client/server application that indexes C/C++ code"""

    homepage = "https://github.com/Andersbakken/rtags/"
    url = "https://github.com/Andersbakken/rtags/releases/download/v2.38/rtags-2.38.tar.gz"
    maintainers("vmiheer")

    license("GPL-3.0-or-later")

    version("2.38", sha256="e19d9cf5823cccc43266ca57c19ae0bb879cbe138511cb3f0343958860481a5d")
    version("2.20", sha256="9d73399421327147dc47b0ae5b95e12e8355f30291ad1954a78c0ef68b4b501f")
    version("2.17", sha256="288fa49fedf647fb15e2ef10f0ebcd9de1a4ef1bbae3a3940870e136d32a3a60")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("llvm@3.3: +clang")
    depends_on("zlib-api")
    depends_on("openssl")
    depends_on("lua@5.3:")
    depends_on("bash-completion")
    depends_on("pkgconfig", type="build")

    patch("add_string_iterator_erase_compile_check.patch", when="@2.12")

    def cmake_args(self):
        args = ["-DCMAKE_EXPORT_COMPILE_COMMANDS=1", "-DRTAGS_NO_ELISP_FILES=1"]
        return args
