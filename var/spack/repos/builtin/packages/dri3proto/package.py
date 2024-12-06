# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dri3proto(AutotoolsPackage, XorgPackage):
    """Direct Rendering Infrastructure 3 Extension.

    This extension defines a protocol to securely allow user applications to
    access the video hardware without requiring data to be passed through the
    X server."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/dri3proto/"
    xorg_mirror_path = "proto/dri3proto-1.0.tar.gz"

    version("1.0", sha256="e1a0dad3009ecde52c0bf44187df5f95cc9a7cc0e76dfc2f2bbf3e909fe03fa9")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
