# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86bigfontproto(AutotoolsPackage, XorgPackage):
    """X.org XF86BigFontProto protocol headers."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86bigfontproto"
    xorg_mirror_path = "proto/xf86bigfontproto-1.2.0.tar.gz"

    version("1.2.0", sha256="d190e6462b2bbbac6ee9a007fb8eccb9ad9f5f70544154f388266f031d4bbb23")
