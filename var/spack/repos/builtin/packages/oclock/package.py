# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Oclock(AutotoolsPackage, XorgPackage):
    """oclock is a simple analog clock using the SHAPE extension to make
    a round (possibly transparent) window."""

    homepage = "https://cgit.freedesktop.org/xorg/app/oclock"
    xorg_mirror_path = "app/oclock-1.0.3.tar.gz"

    version("1.0.5", sha256="ddd93b48ab91222c071816083b7ff55248c63be9c4ae07cdcc3ffd82bf111ce6")
    version("1.0.4", sha256="cffc414cd0cf0b0e4a9bec3b5e707d9c2e2bcd109629d74bd6dd61381563dd35")
    version("1.0.3", sha256="6628d1abe1612b87db9d0170cbe7f1cf4205cd764274f648c3c1bdb745bff877")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxmu")
    depends_on("libxext")
    depends_on("libxt")
    depends_on("libxkbfile")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
