# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkbprint(AutotoolsPackage, XorgPackage):
    """xkbprint generates a printable or encapsulated PostScript description
    of an XKB keyboard description."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xkbprint"
    xorg_mirror_path = "app/xkbprint-1.0.4.tar.gz"

    version("1.0.6", sha256="0d4602034cde190ca3d8f5c1051d34cebff5c0d92f7a32422a4de9d2313698ad")
    version("1.0.5", sha256="af5d91b7e5b05f7d081b66e93fca0112cca049b7b6a644b2637b344d52054ac3")
    version("1.0.4", sha256="169ebbf57fc8b7685c577c73a435998a38c27e0d135ce0a55fccc64cbebec768")

    depends_on("c", type="build")  # generated

    depends_on("libxkbfile")
    depends_on("libx11")

    depends_on("xproto@7.0.17:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
