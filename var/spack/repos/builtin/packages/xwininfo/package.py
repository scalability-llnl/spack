# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwininfo(AutotoolsPackage, XorgPackage):
    """xwininfo prints information about windows on an X server. Various
    information is displayed depending on which options are selected."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xwininfo"
    xorg_mirror_path = "app/xwininfo-1.1.3.tar.gz"

    license("MIT")

    version("1.1.6", sha256="2d52151de9d2808343c715c480e7d37f88958c8b7fcd090178b097436d987c2b")
    version("1.1.5", sha256="aaa915909bb509320c3c775c79babaccc063fd3edc39e520a3c0352e265e9f58")
    version("1.1.4", sha256="3561f6c37eec416ad306f41ff24172b86cbed00854dff8912915e97d2cc17c34")
    version("1.1.3", sha256="784f8b9c9ddab24ce4faa65fde6430a8d7cf3c0564573582452cc99c599bd941")

    depends_on("c", type="build")

    depends_on("libxcb@1.6:")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
