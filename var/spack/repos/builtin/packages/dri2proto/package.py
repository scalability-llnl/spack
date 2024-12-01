# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dri2proto(AutotoolsPackage, XorgPackage):
    """Direct Rendering Infrastructure 2 Extension.

    This extension defines a protocol to securely allow user applications to
    access the video hardware without requiring data to be passed through the
    X server."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/dri2proto/"
    xorg_mirror_path = "proto/dri2proto-2.8.tar.gz"

    license("ICU")

    version("2.8", sha256="7e65b031eaa6ebe23c75583d4abd993ded7add8009b4200a4db7aa10728b0f61")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
