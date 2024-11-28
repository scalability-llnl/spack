# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcmiscproto(AutotoolsPackage, XorgPackage):
    """XC-MISC Extension.

    This extension defines a protocol that provides Xlib two ways to query
    the server for available resource IDs."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xcmiscproto"
    xorg_mirror_path = "proto/xcmiscproto-1.2.2.tar.gz"

    version("1.2.2", sha256="48013cfbe4bd5580925a854a43e2bccbb4c7a5a31128070644617b6dc7f8ef85")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
