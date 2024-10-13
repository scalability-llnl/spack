# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmng(CMakePackage):
    """THE reference library for reading, displaying, writing
    and examining Multiple-Image Network Graphics.  MNG is the animation
    extension to the popular PNG image format."""

    homepage = "https://sourceforge.net/projects/libmng/"
    url = "https://downloads.sourceforge.net/project/libmng/libmng-devel/2.0.3/libmng-2.0.3.tar.gz"

    license("custom")

    version("2.0.3", sha256="cf112a1fb02f5b1c0fce5cab11ea8243852c139e669c44014125874b14b7dfaa")
    version("2.0.2", sha256="4908797bb3541fb5cd8fffbe0b1513ed163509f2a4d57a78b26a96f8d1dd05a2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("jpeg")
    depends_on("zlib-api")
    depends_on("lcms")

    def patch(self):
        # jpeg requires stdio to be included before its headers.
        filter_file(r"^(\#include \<jpeglib\.h\>)", "#include<stdio.h>\n\\1", "libmng_types.h")

    def cmake_args(self):
        return ["-DWITH_LCMS2:BOOL=ON", "-DWITH_LCMS1:BOOL=OFF"]
