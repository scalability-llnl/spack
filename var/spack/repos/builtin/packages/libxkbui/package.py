# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxkbui(AutotoolsPackage, XorgPackage):
    """X.org libxkbui library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxkbui/"
    xorg_mirror_path = "lib/libxkbui-1.0.2.tar.gz"

    version("1.0.2", sha256="196ab4867f3754caae34e51a663cbce26b4af819db3960f1fc4fb42c6a3c535d")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxkbfile")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
