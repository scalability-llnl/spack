# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Inputproto(AutotoolsPackage, XorgPackage):
    """X Input Extension.

    This extension defines a protocol to provide additional input devices
    management such as graphic tablets."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/inputproto"
    xorg_mirror_path = "proto/inputproto-2.3.2.tar.gz"

    version("2.3.2", sha256="10eaadd531f38f7c92ab59ef0708ca195caf3164a75c4ed99f0c04f2913f6ef3")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
