# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86dgaproto(AutotoolsPackage, XorgPackage):
    """X.org XF86DGAProto protocol headers."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86dgaproto"
    xorg_mirror_path = "proto/xf86dgaproto-2.1.tar.gz"

    version("2.1", sha256="73bc6fc830cce5a0ec9c750d4702601fc0fca12d6353ede8b4c0092c9c4ca2af")
