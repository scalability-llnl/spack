# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86driproto(AutotoolsPackage, XorgPackage):
    """XFree86 Direct Rendering Infrastructure Extension.

    This extension defines a protocol to allow user applications to access
    the video hardware without requiring data to be passed through the X
    server."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86driproto"
    xorg_mirror_path = "proto/xf86driproto-2.1.1.tar.gz"

    license("MIT")

    version("2.1.1", sha256="18ff8de129b89fa24a412a1ec1799f8687f96c186c655b44b1a714a3a5d15d6c")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
