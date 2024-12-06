# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Renderproto(AutotoolsPackage, XorgPackage):
    """X Rendering Extension.

    This extension defines the protcol for a digital image composition as
    the foundation of a new rendering model within the X Window System."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/renderproto"
    xorg_mirror_path = "proto/renderproto-0.11.1.tar.gz"

    version("0.11.1", sha256="a0a4be3cad9381ae28279ba5582e679491fc2bec9aab8a65993108bf8dbce5fe")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
