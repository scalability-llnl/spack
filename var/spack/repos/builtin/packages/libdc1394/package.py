# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdc1394(AutotoolsPackage):
    """Library providing an API for IEEE 1394 cameras."""

    homepage = "https://damien.douxchamps.net/ieee1394/libdc1394/"
    url = "https://downloads.sourceforge.net/project/libdc1394/libdc1394-2/2.2.6/libdc1394-2.2.6.tar.gz"

    maintainers("traversaro")

    license("LGPL-2.1-or-later")

    version("2.2.6", sha256="2b905fc9aa4eec6bdcf6a2ae5f5ba021232739f5be047dec8fe8dd6049c10fed")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("libusb")
    depends_on("libraw1394")

    def configure_args(self):
        args = []
        args.append("--disable-dependency-tracking")
        args.append("--disable-examples")
        args.append("--disable-sdltest")
        return args
