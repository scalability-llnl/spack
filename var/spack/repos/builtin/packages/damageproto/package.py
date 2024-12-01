# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Damageproto(AutotoolsPackage, XorgPackage):
    """X Damage Extension.

    This package contains header files and documentation for the X Damage
    extension.  Library and server implementations are separate."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/damageproto"
    xorg_mirror_path = "proto/damageproto-1.2.1.tar.gz"

    version("1.2.1", sha256="f65ccbf1de9750a527ea6e85694085b179f2d06495cbdb742b3edb2149fef303")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
