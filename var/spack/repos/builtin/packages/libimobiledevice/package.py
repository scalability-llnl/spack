# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libimobiledevice(AutotoolsPackage):
    """Library to communicate with iOS devices natively."""

    homepage = "https://www.libimobiledevice.org/"
    url = "https://www.libimobiledevice.org/downloads/libimobiledevice-1.2.0.tar.bz2"
    git = "https://git.libimobiledevice.org/libimobiledevice.git"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("1.2.0", sha256="786b0de0875053bf61b5531a86ae8119e320edab724fc62fe2150cc931f11037")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("pkgconfig", type="build")
    depends_on("libplist")
    depends_on("libtasn1")
    depends_on("libusbmuxd")
    depends_on("openssl")

    def configure_args(self):
        return [
            "--disable-dependency-tracking",
            "--disable-silent-rules",
            "--enable-debug-code",
            "--without-cython",
        ]
