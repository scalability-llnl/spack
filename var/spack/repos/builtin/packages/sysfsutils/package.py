# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sysfsutils(AutotoolsPackage):
    """This package's purpose is to provide a set of utilities for interfacing
    with sysfs, a virtual filesystem in Linux kernel versions 2.5+ that
    provides a tree of system devices. While a filesystem is a very useful
    interface, we've decided to provide a stable programming interface
    that will hopefully make it easier for applications to query system devices
    and their attributes."""

    homepage = "https://github.com/linux-ras/sysfsutils/"
    url = "https://github.com/linux-ras/sysfsutils/archive/sysfsutils_0_5.tar.gz"

    license("GPL-2.0-only AND LGPL-2.1-only", checked_by="tgamblin")

    version("0_5", sha256="6878c8a4281e7de52e57b40fe543b1b4e01d6fbce4ffd45a36e5fc25e376746f")
    version("0_4_0", sha256="9c78edb118c6bd962e04558ddb2df46d456273284fe3f23bb930dc287225aea5")
    version("0_3_0", sha256="f10250aa09513d245cb4ed61ac0dbfd7dfb2e7810bcd8804a07b3fe18f08a74a")

    depends_on("c", type="build")  # generated

    @when("target=aarch64:")
    def configure_args(self):
        args = ["--build=arm-linux"]
        return args
