# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmag(AutotoolsPackage, XorgPackage):
    """xmag displays a magnified snapshot of a portion of an X11 screen."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xmag"
    xorg_mirror_path = "app/xmag-1.0.6.tar.gz"

    license("custom")

    version("1.0.7", sha256="bf94f5ac6ad0dd423b3ee8fb78710d1e47ad7e9fc8b4cf561851fba5370e38eb")
    version("1.0.6", sha256="07c5ec9114376dcd9a3303a38779e79b949d486f3b832d4a438550357d797aa5")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
