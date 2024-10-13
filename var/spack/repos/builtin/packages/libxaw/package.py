# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxaw(AutotoolsPackage, XorgPackage):
    """Xaw is the X Athena Widget Set.
    Xaw is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXaw"
    xorg_mirror_path = "lib/libXaw-1.0.13.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.0.16", sha256="012f90adf8739f2f023d63a5fee1528949cf2aba92ef7ac1abcfc2ae9cf28798")
    version("1.0.15", sha256="ca8a613884c922985202075b3cc8ee8821bfa83a5eb066189ae3cca131e63972")
    version("1.0.14", sha256="59cfed2712cc80bbfe62dd1aacf24f58d74a76dd08329a922077b134a8d8048f")
    version("1.0.13", sha256="7e74ac3e5f67def549722ff0333d6e6276b8becd9d89615cda011e71238ab694")
    version("1.0.12", sha256="e32abc68d759ffb643f842329838f8b6c157e31023cc91059aabf730e7222ad2")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")
    depends_on("libxt")
    depends_on("libxmu")
    depends_on("libxpm")

    depends_on("xproto", type=("build", "link"))
    depends_on("xextproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
