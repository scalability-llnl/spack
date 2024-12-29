# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Xorgproto(MesonPackage, XorgPackage):
    """X Window System unified protocol definitions replacing standalone protos"""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xorgproto"
    xorg_mirror_path = "proto/xorgproto-2024.1.tar.gz"

    maintainers("teaguesterling")

    license("OTHER", checked_by="teaguesterling")

    version("2024.1", sha256="4f6b9b4faf91e5df8265b71843a91fc73dc895be6210c84117a996545df296ce")

    depends_on("meson@0.56:", type="build")
    depends_on("util-macros", type="build")
