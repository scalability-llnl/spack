# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Microsocks(MakefilePackage):
    """Microsocks is a multithreaded, small, efficient SOCKS5 server.
    It is a SOCKS5 service that you can run on your remote boxes to
    tunnel connections through them, if for some reason SSH doesn't
    cut it for you."""

    homepage = "https://github.com/rofl0r/microsocks"
    url = "https://github.com/rofl0r/microsocks/archive/refs/tags/v1.0.2.tar.gz"
    git = "https://github.com/rofl0r/microsocks.git"

    maintainers("jcpunk")

    license("MIT")

    version("develop", branch="master")
    version("1.0.2", sha256="5ece77c283e71f73b9530da46302fdb4f72a0ae139aa734c07fe532407a6211a")

    depends_on("c", type="build")  # generated

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)

    @property
    def install_targets(self):
        return ["prefix={0}".format(self.prefix), "install"]
