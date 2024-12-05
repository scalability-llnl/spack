# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Usbutils(AutotoolsPackage):
    """This is a collection of USB tools for use on Linux and BSD systems
    to query what type of USB devices are connected to the system."""

    homepage = "http://www.linux-usb.org/"
    url = "https://github.com/gregkh/usbutils/archive/v012.tar.gz"

    license("GPL-2.0-or-later")

    version("012", sha256="3f06028134aebd6bb36477019468d7bca2c0014f0f18b9441b7920b7cec7b210")
    version("011", sha256="9cf6e8c3030efc6abbb3c12de4da49816e0d6c6429f43fa3afb874cf72c2c869")
    version("010", sha256="e32f3debe6c1308bb9aa9a92c3d86f8565a6f6cf7711bccb07b0f83bf530717d")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libusb")
