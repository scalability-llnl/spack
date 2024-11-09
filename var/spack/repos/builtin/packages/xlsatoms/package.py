# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlsatoms(AutotoolsPackage, XorgPackage):
    """xlsatoms lists the interned atoms defined on an X11 server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xlsatoms"
    xorg_mirror_path = "app/xlsatoms-1.1.2.tar.gz"

    version("1.1.4", sha256="e3b4dce0e6bf3b60bc308ed184d2dc201ea4af6ce03f0126aa303ccd1ccb1237")
    version("1.1.3", sha256="2a5a3ac0ded207c31ac1c2e9b8ae0030bba7ff604fea87a92781186ba71cbffa")
    version("1.1.2", sha256="5400e22211795e40c4c4d28a048250f92bfb8c373004f0e654a2ad3138c2b36d")

    depends_on("c", type="build")  # generated

    depends_on("libxcb", when="@1.1:")
    depends_on("libx11", when="@:1.0")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
