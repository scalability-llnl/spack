# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdotool(MakefilePackage):
    """fake keyboard/mouse input, window management, and more"""

    homepage = "https://github.com/jordansissel/xdotool"
    url = "https://github.com/jordansissel/xdotool/releases/download/v3.20160805.1/xdotool-3.20160805.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.20211022.1", sha256="96f0facfde6d78eacad35b91b0f46fecd0b35e474c03e00e30da3fdd345f9ada"
    )
    version(
        "3.20160805.1", sha256="35be5ff6edf0c620a0e16f09ea5e101d5173280161772fca18657d83f20fcca8"
    )
    version(
        "3.20160804.2", sha256="2251671c3c3dadab2b70e08bd87f2de6338c7b4e64e7e2d2d881fd13f9bff72c"
    )
    version(
        "3.20160804.1", sha256="7a76ee57515cc767a00a768f1d04c703279d734255a34f8027c29178561fdce9"
    )
    version(
        "3.20150503.1", sha256="e8326883bd5e91bede7336cbee186e6e9143f40b3fb61c84afc9bb31b87e96d1"
    )

    depends_on("c", type="build")  # generated

    depends_on("libxext")
    depends_on("libxtst")
    depends_on("libxi")
    depends_on("libx11")
    depends_on("inputproto")
    depends_on("libxinerama")

    depends_on("libxkbcommon")

    def edit(self, spec, prefix):
        env["PREFIX"] = prefix

        makefile = FileFilter("Makefile")
        makefile.filter("xdotool: LDFLAGS+=-Xlinker", "", string=True)
        makefile.filter("xdotool: LDFLAGS+=-rpath $(INSTALLLIB)", "", string=True)
