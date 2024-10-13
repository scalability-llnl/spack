# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfontenc(AutotoolsPackage, XorgPackage):
    """libfontenc - font encoding library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libfontenc"
    xorg_mirror_path = "lib/libfontenc-1.1.3.tar.gz"

    license("MIT")

    version("1.1.8", sha256="b55039f70959a1b2f02f4ec8db071e5170528d2c9180b30575dccf7510d7fb9f")
    version("1.1.7", sha256="5e5f210329823f08f97bfe9fd5b4105070c789bc5aef88ce01d86d8203d4aa9f")
    version("1.1.3", sha256="6fba26760ca8d5045f2b52ddf641c12cedc19ee30939c6478162b7db8b6220fb")

    depends_on("c", type="build")

    depends_on("zlib-api")

    depends_on("xproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
