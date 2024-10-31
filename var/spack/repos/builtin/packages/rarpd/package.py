# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rarpd(MakefilePackage):
    """RARP (Reverse Address Resolution Protocol) is a protocol which allows
    individual devices on an IP network to get their own IP addresses from the
    RARP server.  Some machines (e.g. SPARC boxes) use this protocol instead
    of e.g. DHCP to query their IP addresses during network bootup."""

    homepage = "https://github.com/fermitools/rarpd"
    url = "https://github.com/fermitools/rarpd/archive/refs/tags/0.981107-fixes.tar.gz"

    maintainers("jcpunk")

    license("GPL-2.0-only")

    version(
        "0.981107-fixes", sha256="92b44adc4a061dcedeb01f7e1c1700374199cccceef1a798de97303d387bb4c2"
    )

    depends_on("c", type="build")  # generated

    @property
    def install_targets(self):
        return ["PREFIX={0}".format(self.prefix), "install"]
