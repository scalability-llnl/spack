# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfs(AutotoolsPackage, XorgPackage):
    """X Font Server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xfs"
    xorg_mirror_path = "app/xfs-1.1.4.tar.gz"

    license("X11")

    version("1.2.1", sha256="76df0106dbf845cb44534eb89f1ed7e9fb4d466125200baeb4719eb2586ded29")
    version("1.2.0", sha256="56ebdc5ff85af332a0c5dc60c9b971551624bbc312bf6af3d13b925600ea367f")
    version("1.1.4", sha256="28f89b854d1ff14fa1efa5b408e5e1c4f6a145420310073c4e44705feeb6d23b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libxfont@1.4.5:", when="@:1.1")
    depends_on("libxfont2@2.0.1:", when="@1.2:")
    depends_on("font-util")

    depends_on("xproto@7.0.17:")
    depends_on("fontsproto")
    depends_on("xtrans")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
