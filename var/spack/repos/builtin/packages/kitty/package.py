# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


# NOTE: This package uses a setup.py file, but does not use distutils/setuptools or any
# other known build system, so this is a custom package
class Kitty(Package):
    """
    fast, featureful, cross-platform, GPU-based terminal emulator
    """

    homepage = "https://sw.kovidgoyal.net/kitty/index.html"
    url = "https://github.com/kovidgoyal/kitty/archive/v0.12.3.tar.gz"
    git = "https://github.com/kovidgoyal/kitty.git"

    license("GPL-3.0-only")

    version("0.12.3", sha256="8d8a1f9c48519e618ac53b614056cf4589edb02fd1d19aa26d5f478e7067887e")
    version("0.12.2", sha256="f1ffb3d10adb9532f9591fc0bbeca527dda50d6d2b6b3934f0799300fd4eefc2")
    version("0.12.1", sha256="a3bf33e3d014635c6951fe4e3f2a0681173a1f44a9fa7a8ed4b60d20de53534a")
    version("0.12.0", sha256="30db676c55cdee0bfe5ff9a30ba569941ba83376a4bb754c8894c1b59ad9ed19")
    version("0.11.3", sha256="f0e1f0972fcee141c05caac543ef017ee7c87ddddf5fde636c614a28e45021c3")
    version("0.11.2", sha256="20d5289732271c33fa4da52c841b8567a2a2b8f514675bb9a2ede9097adb3712")
    version("0.11.1", sha256="3bbc6b5465d424969b16c5ad7f2f67ffbfe33657fdcb443e1bcc11aa00726841")
    version("0.11.0", sha256="abba2b93795609810e4c9b5cefbbada57e370722cee8a00f94a78c0c96226432")
    version("0.10.1", sha256="ef22208497a76e2f88ebe56c176e4608f049b056252cf1bf122c9c1ec711cfa6")
    version("0.10.0", sha256="056563862c5759b740e95efff44b82c1a4efc370092f22f26aee0b774106bf4d")

    depends_on("c", type="build")  # generated

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("harfbuzz@1.5.0:")
    depends_on("libxkbcommon@0.5:")
    depends_on("zlib-api")
    depends_on("libpng")
    depends_on("gl", type=("build", "link", "run"))
    depends_on("pkgconfig", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type="build")
    depends_on("freetype", when=sys.platform != "darwin")
    depends_on("fontconfig", when=sys.platform != "darwin")
    depends_on("xrandr", when=sys.platform != "darwin")
    depends_on("libxinerama", when=sys.platform != "darwin")
    depends_on("xineramaproto", when=sys.platform != "darwin")
    depends_on("libxi", when=sys.platform != "darwin")
    depends_on("libxcursor", when=sys.platform != "darwin")
    depends_on("fixesproto", when=sys.platform != "darwin")
    depends_on("dbus", when=sys.platform != "darwin")
    depends_on("xkeyboard-config", when=sys.platform != "darwin")

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            self.python("-s", "setup.py", "linux-package", "--prefix={0}".format(prefix))
