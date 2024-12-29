# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlsfonts(AutotoolsPackage, XorgPackage):
    """xlsfonts lists fonts available from an X server via the X11
    core protocol."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xlsfonts"
    xorg_mirror_path = "app/xlsfonts-1.0.5.tar.gz"

    version("1.0.7", sha256="b92d4954eaf525674ff83f7e85240ef166c240a774277f71c30674f9f7794171")
    version("1.0.6", sha256="870bbcfb903e790e730ea8ee964c72ce4a4df60f7a4b39541b88193d1e8c9453")
    version("1.0.5", sha256="2a7aeca1023a3918ad2a1af2258ed63d8f8b6c48e53841b3a3f15fb9a0c008ce")

    depends_on("c", type="build")

    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
