# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xf86rushproto(AutotoolsPackage, XorgPackage):
    """X.org XF86RushProto protocol headers."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xf86rushproto"
    xorg_mirror_path = "proto/xf86rushproto-1.1.2.tar.gz"

    version("1.1.2", sha256="7d420ae7e5f0dd94c6010c764c66acc93eed7df7f81bcf93d2a57739970ec841")
