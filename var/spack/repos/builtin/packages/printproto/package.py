# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Printproto(AutotoolsPackage, XorgPackage):
    """Xprint extension to the X11 protocol - a portable, network-transparent
    printing system."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/printproto"
    xorg_mirror_path = "proto/printproto-1.0.5.tar.gz"

    version("1.0.5", sha256="e8b6f405fd865f0ea7a3a2908dfbf06622f57f2f91359ec65d13b955e49843fc")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
