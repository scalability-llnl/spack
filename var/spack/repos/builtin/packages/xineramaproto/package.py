# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xineramaproto(AutotoolsPackage, XorgPackage):
    """X Xinerama Extension.

    This is an X extension that allows multiple physical screens controlled
    by a single X server to appear as a single screen."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xineramaproto"
    xorg_mirror_path = "proto/xineramaproto-1.2.1.tar.gz"

    version("1.2.1", sha256="d99e121edf7b310008d7371ac5dbe3aa2810996d476b754dc78477cc26e5e7c1")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
