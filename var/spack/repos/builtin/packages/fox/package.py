# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fox(AutotoolsPackage):
    """FOX is a C++ based Toolkit for developing Graphical User Interfaces
    easily and effectively. It offers a wide, and growing, collection of
    Controls, and provides state of the art facilities such as drag and drop,
    selection, as well as OpenGL widgets for 3D graphical manipulation. FOX
    also implements icons, images, and user-convenience features such as status
    line help, and tooltips. Tooltips may even be used for 3D objects!"""

    homepage = "http://fox-toolkit.org/"
    url = "http://fox-toolkit.org/ftp/fox-1.7.67.tar.gz"

    license("LGPL-3.0-or-later")

    # Stable releases (even numbers, preferred)
    version("1.7.84", sha256="bdb1fe785605488b58addc95f6091a75873e8a3bea7b83caecfb7f4b0827b34e")
    version("1.7.67", sha256="7e511685119ef096fa90d334da46f0e50cfed8d414df32d80a7850442052f57d")
    version(
        "1.6.57",
        preferred=True,
        sha256="65ef15de9e0f3a396dc36d9ea29c158b78fad47f7184780357b929c94d458923",
    )

    depends_on("cxx", type="build")  # generated

    patch("no_rexdebug.patch", when="@1.7.67")

    variant("opengl", default=False, description="opengl support")

    depends_on("bzip2")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("zlib-api")
    depends_on("libx11")
    depends_on("libsm")
    depends_on("libxft")
    depends_on("libxext")
    depends_on("libxcursor")
    depends_on("libxi")
    depends_on("libxrandr")
    depends_on("gl", when="+opengl")
    depends_on("glu", when="+opengl", type="link")

    def configure_args(self):
        # Make the png link flags explicit or it will try to pick up libpng15
        # from system
        args = [f"LDFLAGS={self.spec['libpng'].libs.search_flags}"]
        args += self.with_or_without("opengl")
        return args
