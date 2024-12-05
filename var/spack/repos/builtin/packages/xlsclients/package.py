# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlsclients(AutotoolsPackage, XorgPackage):
    """xlsclients is a utility for listing information about the client
    applications running on a X11 server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xlsclients"
    xorg_mirror_path = "app/xlsclients-1.1.3.tar.gz"

    version("1.1.5", sha256="225d75e4c0b0929f16f974e20931ab85204b40098d92a5479b0b9379120637e5")
    version("1.1.4", sha256="0b46e8289413c3e7c437a95ecd6494f99d27406d3a0b724ef995a98cbd6c33e8")
    version("1.1.3", sha256="4670a4003aae01e9172efb969246c3d8f33481f290aa8726ff50398c838e6994")

    depends_on("c", type="build")  # generated

    depends_on("libxcb@1.6:", when="@1.1:")
    depends_on("libx11", when="@:1.0")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
