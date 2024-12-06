# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bigreqsproto(AutotoolsPackage, XorgPackage):
    """Big Requests Extension.

    This extension defines a protocol to enable the use of requests
    that exceed 262140 bytes in length."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/bigreqsproto"
    xorg_mirror_path = "proto/bigreqsproto-1.1.2.tar.gz"

    version("1.1.2", sha256="de68a1a9dd1a1219ad73531bff9f662bc62fcd777387549c43cd282399f4a6ea")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
