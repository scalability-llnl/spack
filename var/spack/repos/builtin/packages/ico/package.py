# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ico(AutotoolsPackage, XorgPackage):
    """ico is a simple animation program that may be used for testing various
    X11 operations and extensions.  It displays a wire-frame rotating
    polyhedron, with hidden lines removed, or a solid-fill polyhedron with
    hidden faces removed."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/ico"
    xorg_mirror_path = "app/ico-1.0.4.tar.gz"

    version("1.0.6", sha256="dc59589044d71e3ef4dacf5a62a7b0f69b543386d2a12fb8b5558caee5b1e22f")
    version("1.0.4", sha256="eb8609c3b43dc2e575272f2702590525fe13229e022c4aff8b9a0cc2a3f3205d")

    depends_on("c", type="build")

    depends_on("libx11@0.99.1:")

    depends_on("xproto@7.0.22:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
