# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pcsclite(AutotoolsPackage):
    """PCSC lite project

    Middleware to access a smart card using SCard API (PC/SC)."""

    homepage = "https://pcsclite.apdu.fr"
    url = "https://pcsclite.apdu.fr/files/pcsc-lite-1.9.8.tar.bz2"
    git = "https://salsa.debian.org/rousseau/PCSC.git"

    maintainers("cessenat")

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("1.9.8", sha256="502d80c557ecbee285eb99fe8703eeb667bcfe067577467b50efe3420d1b2289")

    depends_on("c", type="build")  # generated

    # no libudev/systemd package currently in spack
    variant("libudev", default=False, description="Build with libudev")

    depends_on("flex", type="build")
    depends_on("libusb")

    depends_on("autoconf", type="build")
    depends_on("autoconf-archive", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    def autoreconf(self, spec, prefix):
        pass

    @when("@master")
    def autoreconf(self, spec, prefix):
        bootstrap = Executable("./bootstrap")
        bootstrap()

    def configure_args(self):
        args = []
        # no libudev/systemd package currently in spack
        args.append("--disable-libsystemd")
        args.extend(self.enable_or_disable("libudev"))
        args.append("--with-systemdsystemunitdir=no")
        return args
