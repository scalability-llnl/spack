# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nettle(AutotoolsPackage, GNUMirrorPackage):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "https://www.lysator.liu.se/~nisse/nettle/"
    gnu_mirror_path = "nettle/nettle-3.3.tar.gz"

    license("GPL-2.0-or-later OR LGPL-3.0-or-later")

    version("3.9.1", sha256="ccfeff981b0ca71bbd6fbcb054f407c60ffb644389a5be80d6716d5b550c6ce3")
    version("3.8.1", sha256="364f3e2b77cd7dcde83fd7c45219c834e54b0c75e428b6f894a23d12dd41cbfe")
    version("3.4.1", sha256="f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad")
    version("3.4", sha256="ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94")
    version("3.3", sha256="46942627d5d0ca11720fec18d81fc38f7ef837ea4197c1f630e71ce0d470b11e")
    version("3.2", sha256="ea4283def236413edab5a4cf9cf32adf540c8df1b9b67641cfc2302fca849d97")
    version("2.7.1", sha256="bc71ebd43435537d767799e414fce88e521b7278d48c860651216e1fc6555b40")
    version("2.7", sha256="c294ea133c05382cc2effb1734d49f4abeb1ad8515543a333de49a11422cd4d6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gmp")
    depends_on("m4", type="build")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)

    def configure_args(self):
        return ["--disable-openssl"]
