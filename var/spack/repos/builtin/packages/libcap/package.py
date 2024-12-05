# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcap(MakefilePackage):
    """Libcap implements the user-space interfaces to the POSIX 1003.1e
    capabilities available in Linux kernels. These capabilities are a
    partitioning of the all powerful root privilege into a set of
    distinct privileges."""

    homepage = "https://sites.google.com/site/fullycapable/"
    url = "https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-2.25.tar.gz"

    license("BSD-3-Clause OR GPL-2.0-only")

    version("2.69", sha256="3a99ec26452e328e0ea408efd67096ef914f4ee4788fa8e8e21f214e2bd670b9")
    version("2.68", sha256="046e55716e0643b565efcd1dab1d26c5625709fcd0b5c271290c7ea1524cf906")
    version("2.67", sha256="2d0b679a431c06afd8651a8ada906303eda8b3ac67c308e5fe1937eea5c018aa")
    version("2.66", sha256="5f65dc5b2e9f63a0748ea1b05be7965a38548db1cbfd53b30271ff02186b3a4a")
    version("2.65", sha256="25718d9c45ef6beccb55b509ed4bae94ae2bdfeb808709662b264aec0a7016f4")
    version("2.64", sha256="e9ec608ae5720989d7274531f9898d64b6bca2491a231b8091229e49891933dd")
    version("2.25", sha256="4ca80dc6f9f23d14747e4b619fd9784434c570e24a7346f326c692784ed83a86")

    depends_on("c", type="build")  # generated

    patch("libcap-fix-the-libcap-native-building-failure-on-CentOS-6.7.patch", when="@2.25")

    def makeflags(self, prefix):
        return [
            "RAISE_SETFCAP=no",
            "GOLANG=no",
            "USE_GPERF=no",
            "SHARED=yes",
            "lib=lib",
            f"prefix={prefix}",
        ]

    def build(self, spec, prefix):
        make(*self.makeflags(prefix))

    def install(self, spec, prefix):
        make(*self.makeflags(prefix), "install")

        # this is a shared library that prints some info when executed
        set_executable(join_path(prefix.lib, "libcap.so"))
