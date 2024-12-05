# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glproto(AutotoolsPackage, XorgPackage):
    """OpenGL Extension to the X Window System.

    This extension defines a protocol for the client to send 3D rendering
    commands to the X server."""

    homepage = "https://www.x.org/wiki/"
    xorg_mirror_path = "proto/glproto-1.4.17.tar.gz"

    license("SGI-B-1.1")

    version("1.4.17", sha256="9d8130fec2b98bd032db7730fa092dd9dec39f3de34f4bb03ceb43b9903dbc96")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
