# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libusb(AutotoolsPackage):
    """Library for USB device access."""

    homepage = "https://libusb.info/"
    url = "https://github.com/libusb/libusb/releases/download/v1.0.22/libusb-1.0.22.tar.bz2"
    git = "https://github.com/libusb/libusb"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("1.0.22", sha256="75aeb9d59a4fdb800d329a545c2e6799f732362193b465ea198f2aa275518157")
    version("1.0.21", sha256="7dce9cce9a81194b7065ee912bcd55eeffebab694ea403ffb91b67db66b1824b")
    version("1.0.20", sha256="cb057190ba0a961768224e4dc6883104c6f945b2bf2ef90d7da39e7c1834f7ff")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    @when("@master")
    def patch(self):
        mkdir("m4")

    def configure_args(self):
        args = []
        args.append("--disable-dependency-tracking")
        # no libudev/systemd package currently in spack
        args.append("--disable-udev")
        return args
