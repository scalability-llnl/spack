# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xscope(AutotoolsPackage, XorgPackage):
    """XSCOPE -- a program to monitor X11/Client conversations."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xscope"
    xorg_mirror_path = "app/xscope-1.4.1.tar.gz"

    license("MIT")

    version("1.4.3", sha256="86f9da3cf0422b5964191c9e8f792e107577818de094b38db0a6dbce403a9b54")
    version("1.4.2", sha256="e12d634a69ce1ec36b0afd1d40814215e262801a030ddf83d7d0348cd046b381")
    version("1.4.1", sha256="f99558a64e828cd2c352091ed362ad2ef42b1c55ef5c01cbf782be9735bb6de3")

    depends_on("c", type="build")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("xtrans")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
