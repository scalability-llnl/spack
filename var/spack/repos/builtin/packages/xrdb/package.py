# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xrdb(AutotoolsPackage, XorgPackage):
    """xrdb - X server resource database utility."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrdb"
    xorg_mirror_path = "app/xrdb-1.1.0.tar.gz"

    license("MIT")

    version("1.2.1", sha256="e674f5fb081a023e54878c0aac728dc30feb821207c989cff17a60f0c4a80ced")
    version("1.2.0", sha256="7dec50e243d55c6a0623ff828355259b6a110de74a0c65c40529514324ef7938")
    version("1.1.1", sha256="d19f856296c5f1742a703afc620654efc76fedfb86e1afe0bff9f1038b9e8a47")
    version("1.1.0", sha256="44b0b6b7b7eb80b83486dfea67c880f6b0059052386c7ddec4d58fd2ad9ae8e9")

    depends_on("c", type="build")

    depends_on("libxmu")
    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
