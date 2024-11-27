# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tulip(CMakePackage):
    """Tulip is an information visualization framework dedicated to the
    analysis and visualization of relational data.

    Tulip aims to provide the developer with a complete library, supporting
    the design of interactive information visualization applications for
    relational data that can be tailored to the problems he or she is
    addressing.
    """

    homepage = "https://tulip.labri.fr"
    url = "https://sourceforge.net/projects/auber/files/tulip/tulip-5.4.0/tulip-5.4.0_src.tar.gz"

    license("LGPL-3.0-only")

    version("5.4.0", sha256="2175e4e1a79028ab7a2479e882242f304fd3e01fedf80e1f29f8f5e9a6eb1325")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    extends("python")
    depends_on("py-pyqt5", type=("build", "run"))

    depends_on("yajl")
    depends_on("qt")
    depends_on("qhull")
    depends_on("freetype")
    depends_on("zlib-api")
    depends_on("glew")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libxml2")

    def cmake_args(self):
        # The use of GL/glu.h seems to be deprecated, see:
        # https://github.com/nigels-com/glew/issues/192
        return [
            '-DCMAKE_CXX_FLAGS="-DGLEW_NO_GLU"',
            '-DCMAKE_C_FLAGS="-DGLEW_NO_GLU"',
            "-DTULIP_BUILD_DOC:BOOL=OFF",
        ]
