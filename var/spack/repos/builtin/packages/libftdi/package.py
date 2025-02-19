# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libftdi(CMakePackage):
    """libftdi - A library (using libusb) to talk to FTDI's UART/FIFO chips
    including the popular bitbang mode"""

    license("GPL-2.0-or-later")

    homepage = "https://www.intra2net.com/en/developer/libftdi/index.php"
    git = "git://developer.intra2net.com/libftdi"

    maintainers("davekeeshan")


    version("master", branch="master")
    version("1.5", commit="5c2c58e03ea999534e8cb64906c8ae8b15536c30")
    version("1.4", commit="d5c1622a2ff0c722c0dc59533748489b45774e55")
    version("1.3", commit="96d337a16b723d792f6ab5f40b7aa43120ac4782")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libusb", type="build")
    depends_on("libconfuse", type="build")
