# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xprehashprinterlist(AutotoolsPackage, XorgPackage):
    """Rehash list of Xprint printers."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xprehashprinterlist"
    xorg_mirror_path = "app/xprehashprinterlist-1.0.1.tar.gz"

    version("1.0.1", sha256="396986da064b584138cfcff79a8aed12590a9dab24f1cd2d80b08bc1cb896a43")

    depends_on("c", type="build")  # generated

    depends_on("libxp")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
