# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xman(AutotoolsPackage, XorgPackage):
    """xman is a graphical manual page browser using the Athena Widgets (Xaw)
    toolkit."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xman"
    xorg_mirror_path = "app/xman-1.1.4.tar.gz"

    license("X11")

    version("1.1.5", sha256="ff0aeb164fcb736b381bd7722c27aa0284cafb9a5d1b3940c3c3ee0af642f204")
    version("1.1.4", sha256="72fd0d479624a31d9a7330e5fdd220b7aa144744781f8e78aa12deece86e05c7")

    depends_on("c", type="build")

    depends_on("libxaw")
    depends_on("libxt")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
