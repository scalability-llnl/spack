# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Recordproto(AutotoolsPackage, XorgPackage):
    """X Record Extension.

    This extension defines a protocol for the recording and playback of user
    actions in the X Window System."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/recordproto"
    xorg_mirror_path = "proto/recordproto-1.14.2.tar.gz"

    version("1.14.2", sha256="485f792570dd7afe49144227f325bf2827bc7d87aae6a8ab6c1de2b06b1c68c5")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
