# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxi(AutotoolsPackage, XorgPackage):
    """libXi - library for the X Input Extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXi"
    xorg_mirror_path = "lib/libXi-1.7.6.tar.gz"

    license("MIT AND X11")

    maintainers("wdconinc")

    # Newer versions are blocked by https://github.com/spack/spack/issues/41688
    # version("1.8.1", sha256="3b5f47c223e4b63d7f7fe758886b8bf665b20a7edb6962c423892fd150e326ea")
    # version("1.8", sha256="c80fd200a1190e4406bb4cc6958839d9651638cb47fa546a595d4bebcd3b9e2d")
    version("1.7.10", sha256="b51e106c445a49409f3da877aa2f9129839001b24697d75a54e5c60507e9a5e3")
    version("1.7.9", sha256="463cc5370191404bc0f8a450fdbf6d9159efbbf274e5e0f427a60191fed9cf4b")
    version("1.7.8", sha256="7466d0c626a9cc2e53fd78c811815e82924cd7582236a82401df3d282a9c2889")
    version("1.7.7", sha256="501f49e9c85609da17614d711aa4931fd128011042ff1cae53a16ce03e51ff5e")
    version("1.7.6", sha256="4e88fa7decd287e58140ea72238f8d54e4791de302938c83695fc0c9ac102b7e")

    depends_on("c", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("libx11@1.6:")
    depends_on("libxext@1.0.99.1:")
    depends_on("libxfixes@5:")
    depends_on("fixesproto@5.0:", type="build")
    depends_on("xproto@7.0.13:", type="build")
    depends_on("xextproto@7.0.3:", type="build")
    depends_on("inputproto@2.2.99.1:", when="@1.7:", type=("build", "link"))
    # depends_on("inputproto@2.3.99.1:", when="@1.8:", type=("build", "link"))

    @property
    def libs(self):
        return find_libraries("libXi", self.prefix, shared=True, recursive=True)
