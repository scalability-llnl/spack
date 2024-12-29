# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fslsfonts(AutotoolsPackage, XorgPackage):
    """fslsfonts produces a list of fonts served by an X font server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/fslsfonts"
    xorg_mirror_path = "app/fslsfonts-1.0.5.tar.gz"

    version("1.0.6", sha256="17179e32cfc4588da9e8aa1aa21f862af265d673de64fe5e3a8556921caccb28")
    version("1.0.5", sha256="27e58d2313835ce0f08cf47c59a43798b122f605a55f54b170db27b57a492007")

    depends_on("c", type="build")

    depends_on("libfs")

    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
