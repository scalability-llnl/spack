# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxv(AutotoolsPackage, XorgPackage):
    """libXv - library for the X Video (Xv) extension to the
    X Window System."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXv"
    xorg_mirror_path = "lib/libXv-1.0.10.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.0.12", sha256="ce706619a970a580a0e35e9b5c98bdd2af243ac6494c65f44608a89a86100126")
    version("1.0.11", sha256="c4112532889b210e21cf05f46f0f2f8354ff7e1b58061e12d7a76c95c0d47bb1")
    version("1.0.10", sha256="89a664928b625558268de81c633e300948b3752b0593453d7815f8775bab5293")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("videoproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
