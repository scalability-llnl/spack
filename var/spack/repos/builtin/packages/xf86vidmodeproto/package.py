# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86vidmodeproto(AutotoolsPackage, XorgPackage):
    """XFree86 Video Mode Extension.

    This extension defines a protocol for dynamically configuring modelines
    and gamma."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86vidmodeproto"
    xorg_mirror_path = "proto/xf86vidmodeproto-2.3.1.tar.gz"

    version("2.3.1", sha256="c3512b11cefa7558576551f8582c6e7071c8a24d78176059d94b84b48b262979")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
