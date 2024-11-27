# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xedit(AutotoolsPackage, XorgPackage):
    """Xedit is a simple text editor for X."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xedit"
    xorg_mirror_path = "app/xedit-1.2.2.tar.gz"

    license("BSD-3-Clause")

    version("1.2.3", sha256="3c8be175613f72858b24d973b0d66ae2d3c9a48a5f0bd637920d85b283feede7")
    version("1.2.2", sha256="7e2dacbc2caed81d462ee028e108866893217d55e35e4b860b09be2b409ee18f")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libxt@1.0:")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
