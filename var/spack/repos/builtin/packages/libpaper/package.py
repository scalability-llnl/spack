# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpaper(AutotoolsPackage):
    """The paper library and accompanying files are intended to provide a
    simple way for applications to take actions based on a system- or
    user-specified paper size."""

    homepage = "https://packages.debian.org/unstable/source/libpaper"
    url = "https://deb.debian.org/debian/pool/main/libp/libpaper/libpaper_1.1.28.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.1.29", sha256="26330e21e9a3124658d515fd850b0cde546ff42d89b2596a5264c5f1677f0547")
    version("1.1.28", sha256="c8bb946ec93d3c2c72bbb1d7257e90172a22a44a07a07fb6b802a5bb2c95fddc")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
