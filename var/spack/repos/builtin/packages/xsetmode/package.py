# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsetmode(AutotoolsPackage, XorgPackage):
    """Set the mode for an X Input device."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xsetmode"
    xorg_mirror_path = "app/xsetmode-1.0.0.tar.gz"

    version("1.0.0", sha256="9ee0d6cf72dfaacb997f9570779dcbc42f5395ae102180cb19382860b4b02ef3")

    depends_on("c", type="build")  # generated

    depends_on("libxi")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
