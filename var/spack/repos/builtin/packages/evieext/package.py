# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Evieext(AutotoolsPackage, XorgPackage):
    """Extended Visual Information Extension (XEVIE).

    This extension defines a protocol for a client to determine information
    about core X visuals beyond what the core protocol provides."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/evieproto"
    xorg_mirror_path = "proto/evieext-1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="e58080443c279dfb5a23c37076922df535e42bf209d21a1f3e88442cc01b4a0e")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
