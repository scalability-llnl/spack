# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fonttosfnt(AutotoolsPackage, XorgPackage):
    """Wrap a bitmap font in a sfnt (TrueType) wrapper."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/fonttosfnt"
    xorg_mirror_path = "app/fonttosfnt-1.0.4.tar.gz"

    license("MIT")

    version("1.2.3", sha256="f7197c327b3b697afd668d064d1996e0ce709f28adaee6e80b784f5c2d0826db")
    version("1.2.2", sha256="8111317c38f63aff08c717595e65381af7ebfc54ccc23511c2042ef1cd86c648")
    version("1.0.4", sha256="3873636be5b3b8e4160070e8f9a7a9221b5bd5efbf740d7abaa9092e10732673")

    depends_on("c", type="build")

    depends_on("freetype")
    depends_on("libfontenc")

    depends_on("xproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
