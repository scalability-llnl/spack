# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcompmgr(AutotoolsPackage, XorgPackage):
    """xcompmgr is a sample compositing manager for X servers supporting the
    XFIXES, DAMAGE, RENDER, and COMPOSITE extensions.  It enables basic
    eye-candy effects."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xcompmgr"
    xorg_mirror_path = "app/xcompmgr-1.1.7.tar.gz"

    license("MIT")

    version("1.1.9", sha256="978294a31bf8decb90acae750c9630b986b78a98c3e0517bd63486a62fa10030")
    version("1.1.8", sha256="ba10933678a5665d06fa7096bd08f37316add8ed84aaacd7ba26a97e8f2e0498")
    version("1.1.7", sha256="ef4b23c370f99403bbd9b6227f8aa4edc3bc83fc6d57ee71f6f442397cef505a")

    depends_on("c", type="build")  # generated

    depends_on("libxcomposite")
    depends_on("libxfixes")
    depends_on("libxdamage")
    depends_on("libxrender")
    depends_on("libxext")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
