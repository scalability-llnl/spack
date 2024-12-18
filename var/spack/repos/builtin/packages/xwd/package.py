# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwd(AutotoolsPackage, XorgPackage):
    """xwd - dump an image of an X window."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xwd"
    xorg_mirror_path = "app/xwd-1.0.6.tar.gz"

    license("custom")

    version("1.0.8", sha256="066d10a1b66a47efd7caa7d7aa670c0c26ff90c8408f0e30b4dfb29dcb39d4c4")
    version("1.0.7", sha256="1c5e86806234a96a29c90be1872128293c6def5ba69ecb70e161efe325e2ba03")
    version("1.0.6", sha256="ff01f0a4b736f955aaf7c8c3942211bc52f9fb75d96f2b19777f33fff5dc5b83")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxkbfile")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
