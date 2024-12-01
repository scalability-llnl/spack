# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kbproto(AutotoolsPackage, XorgPackage):
    """X Keyboard Extension.

    This extension defines a protcol to provide a number of new capabilities
    and controls for text keyboards."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/kbproto"
    xorg_mirror_path = "proto/kbproto-1.0.7.tar.gz"

    version("1.0.7", sha256="828cb275b91268b1a3ea950d5c0c5eb076c678fdf005d517411f89cc8c3bb416")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
