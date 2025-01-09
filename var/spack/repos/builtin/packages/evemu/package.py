# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Evemu(AutotoolsPackage):
    """The evemu library and tools are used to describe devices, record data,
    create devices and replay data from kernel evdev devices."""

    homepage = "https://gitlab.freedesktop.org/libevdev/evemu"
    url = "https://gitlab.freedesktop.org/libevdev/evemu/-/archive/v2.7.0/evemu-v2.7.0.tar.gz"

    license("LGPL-3.0-only")

    version("2.7.0", sha256="b4ba7458ccb394e9afdb2562c9809e9e90fd1099e8a028d05de3f12349ab6afa")
    version("2.6.0", sha256="2efa4abb51f9f35a48605db51ab835cf688f02f6041d48607e78e11ec3524ac8")
    version("2.5.0", sha256="1d88b2a81db36b6018cdc3e8d57fbb95e3a5df9e6806cd7b3d29c579a7113d4f")
    version("2.4.0", sha256="ea8e7147550432321418ae1161a909e054ff482c86a6a1631f727171791a501d")
    version("2.3.1", sha256="fbe77a083ed4328e76e2882fb164efc925b308b83e879b518136ee54d74def46")

    depends_on("c", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libevdev@1.2.99.902:")
