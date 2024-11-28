# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfont(AutotoolsPackage, XorgPackage):
    """libXfont provides the core of the legacy X11 font system, handling the
    index files (fonts.dir, fonts.alias, fonts.scale), the various font file
    formats, and rasterizing them.   It is used by the X servers, the
    X Font Server (xfs), and some font utilities (bdftopcf for instance),
    but should not be used by normal X11 clients.  X11 clients access fonts
    via either the new API's in libXft, or the legacy API's in libX11."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXfont"
    xorg_mirror_path = "lib/libXfont-1.5.2.tar.gz"

    license("MIT")

    version("1.5.4", sha256="59be6eab53f7b0feb6b7933c11d67d076ae2c0fd8921229c703fc7a4e9a80d6e")
    version("1.5.2", sha256="a7350c75171d03d06ae0d623e42240356d6d3e1ac7dfe606639bf20f0d653c93")

    depends_on("c", type="build")

    depends_on("libfontenc")
    depends_on("freetype build_system=autotools")

    depends_on("xtrans")
    depends_on("xproto", type=("build", "link"))
    depends_on("fontsproto@2.1.3:", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
