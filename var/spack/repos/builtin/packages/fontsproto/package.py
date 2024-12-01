# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fontsproto(AutotoolsPackage, XorgPackage):
    """X Fonts Extension."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/fontsproto"
    xorg_mirror_path = "proto/fontsproto-2.1.3.tar.gz"

    version("2.1.3", sha256="72c44e63044b2b66f6fa112921621ecc20c71193982de4f198d9a29cda385c5e")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
