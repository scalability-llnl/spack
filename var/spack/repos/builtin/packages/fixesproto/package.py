# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fixesproto(AutotoolsPackage, XorgPackage):
    """X Fixes Extension.

    The extension makes changes to many areas of the protocol to resolve
    issues raised by application interaction with core protocol mechanisms
    that cannot be adequately worked around on the client side of the wire."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/fixesproto"
    xorg_mirror_path = "proto/fixesproto-5.0.tar.gz"

    version("5.0", sha256="67865a0e3cdc7dec1fd676f0927f7011ad4036c18eb320a2b41dbd56282f33b8")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
    depends_on("xextproto")
