# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsetpointer(AutotoolsPackage, XorgPackage):
    """Set an X Input device as the main pointer."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xsetpointer"
    xorg_mirror_path = "app/xsetpointer-1.0.1.tar.gz"

    version("1.0.1", sha256="54be93b20fd6f1deac67246d6e214a60b02dcfbf05295e43751f7a04edb986ac")

    depends_on("c", type="build")

    depends_on("libxi", type="link")
    depends_on("libx11", type="link")
    depends_on("inputproto@1.4:", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
