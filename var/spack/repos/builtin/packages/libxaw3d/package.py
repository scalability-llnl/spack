# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxaw3d(AutotoolsPackage, XorgPackage):
    """Xaw3d is the X 3D Athena Widget Set.
    Xaw3d is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXaw3d"
    xorg_mirror_path = "lib/libXaw3d-1.6.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.6.6", sha256="0cdb8f51c390b0f9f5bec74454e53b15b6b815bc280f6b7c969400c9ef595803")
    version("1.6.5", sha256="1123d80c58f45616ef18502081eeec5e92f20c7e7dd82a24f9e2e4f3c0e86dc7")
    version("1.6.4", sha256="09fecfdab9d7d5953567883e2074eb231bc7a122a06e5055f9c119090f1f76a7")
    version("1.6.2", sha256="847dab01aeac1448916e3b4edb4425594b3ac2896562d9c7141aa4ac6c898ba9")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxmu")
    depends_on("libxext")
    depends_on("libxpm")
    depends_on("xproto@7.0.22:", type=("build", "link"))

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
