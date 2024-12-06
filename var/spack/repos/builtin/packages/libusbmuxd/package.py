# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libusbmuxd(AutotoolsPackage):
    """A client library to multiplex connections from and to iOS devices."""

    homepage = "https://www.libimobiledevice.org/"
    url = "https://www.libimobiledevice.org/downloads/libusbmuxd-1.0.10.tar.bz2"
    git = "https://git.libimobiledevice.org/libusbmuxd.git"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("1.0.10", sha256="1aa21391265d2284ac3ccb7cf278126d10d354878589905b35e8102104fec9f2")
    version("1.0.9", sha256="2e3f708a3df30ad7832d2d2389eeb29f68f4e4488a42a20149cc99f4f9223dfc")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("pkgconfig", type="build")
    depends_on("libplist")

    def configure_args(self):
        return ["--disable-dependency-tracking", "--disable-silent-rules"]
