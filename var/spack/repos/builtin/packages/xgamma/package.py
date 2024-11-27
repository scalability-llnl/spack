# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xgamma(AutotoolsPackage, XorgPackage):
    """xgamma allows X users to query and alter the gamma correction of a
    monitor via the X video mode extension (XFree86-VidModeExtension)."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xgamma"
    xorg_mirror_path = "app/xgamma-1.0.6.tar.gz"

    license("custom")

    version("1.0.7", sha256="61f5ef02883d65ab464678ad3d8c5445a0ff727fe6255af90b1b842ddf77370d")
    version("1.0.6", sha256="66da1d67e84146518b69481c6283c5d8f1027ace9ff7e214d3f81954842e796a")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxxf86vm")

    depends_on("xproto@7.0.17:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
