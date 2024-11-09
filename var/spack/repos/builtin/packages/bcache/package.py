# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bcache(MakefilePackage):
    """Bcache is a patch for the Linux kernel to use SSDs to cache other block
    devices."""

    homepage = "https://bcache.evilpiepirate.org/"
    url = "https://github.com/g2p/bcache-tools/archive/v1.0.8.tar.gz"

    license("GPL-2.0-only")

    version("1.0.8", sha256="d56923936f37287efc57a46315679102ef2c86cd0be5874590320acd48c1201c")
    version("1.0.7", sha256="64d76d1085afba8c3d5037beb67bf9d69ee163f357016e267bf328c0b1807abd")
    version("1.0.6", sha256="9677c6da3ceac4e1799d560617c4d00ea7e9d26031928f8f94b8ab327496d4e0")
    version("1.0.5", sha256="1449294ef545b3dc6f715f7b063bc2c8656984ad73bcd81a0dc048cbba416ea9")
    version("1.0.4", sha256="102ffc3a8389180f4b491188c3520f8a4b1a84e5a7ca26d2bd6de1821f4d913d")

    depends_on("c", type="build")  # generated

    depends_on("uuid")
    depends_on("util-linux")
    depends_on("gettext")
    depends_on("pkgconfig", type="build")

    patch(
        "func_crc64.patch",
        sha256="558b35cadab4f410ce8f87f0766424a429ca0611aa2fd247326ad10da115737d",
    )

    def flag_handler(self, name, flags):
        if name == "ldflags" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        return self.env_flags(name, flags)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bcache-register", prefix.bin)
        install("bcache-super-show", prefix.bin)
        install("make-bcache", prefix.bin)
        install("probe-bcache", prefix.bin)
