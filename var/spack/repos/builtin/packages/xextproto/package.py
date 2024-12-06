# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xextproto(AutotoolsPackage, XorgPackage):
    """X Protocol Extensions."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xextproto"
    xorg_mirror_path = "proto/xextproto-7.3.0.tar.gz"

    version("7.3.0", sha256="1b1bcdf91221e78c6c33738667a57bd9aaa63d5953174ad8ed9929296741c9f5")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    parallel = False
