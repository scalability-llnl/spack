# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libapplewm(AutotoolsPackage, XorgPackage):
    """AppleWM is a simple library designed to interface with the Apple-WM
    extension. This extension allows X window managers to better interact with
    the Mac OS X Aqua user interface when running X11 in a rootless mode."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libAppleWM"
    xorg_mirror_path = "lib/libAppleWM-1.4.1.tar.gz"

    license("MIT")

    version("1.4.1", sha256="d7fb098d65ad4d840f60e5c92de7f58f1725bd70d0d132755ea453462fd50049")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("applewmproto@1.4:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    conflicts("platform=linux", msg="AppleWM is only available for macOS")
    conflicts("platform=windows", msg="AppleWM is only available for macOS")
