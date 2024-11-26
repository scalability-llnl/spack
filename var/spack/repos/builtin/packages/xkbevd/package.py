# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xkbevd(AutotoolsPackage, XorgPackage):
    """XKB event daemon demo."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xkbevd"
    xorg_mirror_path = "app/xkbevd-1.1.4.tar.gz"

    version("1.1.5", sha256="5d6b65a417be57e19a76277601da83271b19de6e71cb0e8821441f6fb9973c47")
    version("1.1.4", sha256="97dc2c19617da115c3d1183807338fa78c3fd074d8355d10a484f7b1c5b18459")

    depends_on("c", type="build")  # generated

    depends_on("libxkbfile")
    depends_on("libx11")

    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
