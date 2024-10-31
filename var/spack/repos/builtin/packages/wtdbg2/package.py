# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wtdbg2(MakefilePackage):
    """A fuzzy Bruijn graph approach to long noisy reads assembly"""

    homepage = "https://github.com/ruanjue/wtdbg2"
    url = "https://github.com/ruanjue/wtdbg2/archive/v2.3.tar.gz"

    license("GPL-3.0-only")

    version("2.5", sha256="a2ffc8503d29f491a9a38ef63230d5b3c96db78377b5d25c91df511d0df06413")
    version("2.3", sha256="fb61d38a4c60a39b3b194e63b855141c05ddcbe71cf244ae613766a9b0a56621")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("sse2neon", when="target=aarch64:")

    patch("for_aarch64.patch", when="target=aarch64:")

    def edit(self, spec, prefix):
        if spec.target.family == "aarch64":
            makefile = FileFilter("Makefile")
            makefile.filter("-mpopcnt -msse4.2", "")

    def install(self, spec, prefix):
        make("install", f"BIN={prefix.bin}")
