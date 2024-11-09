# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxt(AutotoolsPackage, XorgPackage):
    """libXt - X Toolkit Intrinsics library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXt"
    xorg_mirror_path = "lib/libXt-1.1.5.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.3.0", sha256="de4a80c4cc7785b9620e572de71026805f68e85a2bf16c386009ef0e50be3f77")
    version("1.2.1", sha256="6da1bfa9dd0ed87430a5ce95b129485086394df308998ebe34d98e378e3dfb33")
    version("1.2.0", sha256="d4bee88898fc5e1dc470e361430c72fbc529b9cdbbb6c0ed3affea3a39f97d8d")
    version("1.1.5", sha256="b59bee38a9935565fa49dc1bfe84cb30173e2e07e1dcdf801430d4b54eb0caa3")

    depends_on("c", type="build")

    depends_on("libsm")
    depends_on("libice")
    depends_on("libx11")

    depends_on("xproto", type=("build", "link"))
    depends_on("kbproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXt", root=self.prefix, shared=True, recursive=True)
