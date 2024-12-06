# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpostal(AutotoolsPackage):
    """A C library for parsing/normalizing street addresses around the world.
    Powered by statistical NLP and open geo data."""

    homepage = "https://github.com/openvenues/libpostal"
    url = "https://github.com/openvenues/libpostal/archive/refs/tags/v1.1.tar.gz"

    maintainers("jgaeb")

    license("MIT")

    version("1.1", sha256="8cc473a05126895f183f2578ca234428d8b58ab6fadf550deaacd3bd0ae46032")
    version("1.0.0", sha256="3035af7e15b2894069753975d953fa15a86d968103913dbf8ce4b8aa26231644")
    version("0.3.4", sha256="8b3b95660c5b5d4fe48045b9acb000d1a0eb19d58d0c2d2041e78d9a96d88716")
    version("0.3.3", sha256="dc73de37d7f7b96f329fd213dcbac540f2ae92fbef9c079fd64fbc8daeb87b01")
    version("0.3.2", sha256="9a1590eadf4ebe84979113b71059410413adf239b2999d22d11fe8778945f2c1")
    version("0.3.1", sha256="68c51a5fdae41e1cac474742789ba5a46a38e307a0a2450cb2d3e33b4f17cf4d")
    version("0.3", sha256="28c19e21bab13425a76aa65a8435f4b3909611056c2ff439c39b4e57b2a70150")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("curl", type="build")
    depends_on("pkgconfig", type="build")

    def autoreconf(self, spec, prefix):
        which("sh")("bootstrap.sh")

    def configure_args(self):
        args = ["--datadir={0}".format(self.prefix.share)]

        # Check if the target is Apple's ARM-based M1 chip.
        arch = self.spec.architecture
        if arch.platform == "darwin" and arch.target == "m1":
            args.append("--disable-sse2")

        return args
