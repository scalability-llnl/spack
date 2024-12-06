# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dmxproto(AutotoolsPackage, XorgPackage):
    """Distributed Multihead X (DMX) Extension.

    This extension defines a protocol for clients to access a front-end proxy
    X server that controls multiple back-end X servers making up a large
    display."""

    homepage = "https://dmx.sourceforge.net/"
    xorg_mirror_path = "proto/dmxproto-2.3.1.tar.gz"

    version("2.3.1", sha256="3262bbf5902211a3ce88f5c6ab4528145ff84f69c52fd386ae0312bc45fb8a40")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
