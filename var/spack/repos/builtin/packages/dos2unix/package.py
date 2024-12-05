# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Dos2unix(MakefilePackage):
    """DOS/Mac to Unix and vice versa text file format converter."""

    homepage = "https://waterlan.home.xs4all.nl/dos2unix.html"
    url = "https://waterlan.home.xs4all.nl/dos2unix/dos2unix-7.3.4.tar.gz"

    maintainers("cessenat")

    license("BSD-2-Clause")

    version("7.4.4", sha256="28a841db0bd5827d645caba9d8015e3a71983dc6e398070b5287ee137ae4436e")
    version("7.4.2", sha256="6035c58df6ea2832e868b599dfa0d60ad41ca3ecc8aa27822c4b7a9789d3ae01")
    version("7.3.4", sha256="8ccda7bbc5a2f903dafd95900abb5bf5e77a769b572ef25150fde4056c5f30c5")

    depends_on("c", type="build")  # generated

    depends_on("gettext")

    executables = [r"^dos2unix$"]

    @property
    def build_targets(self):
        targets = [
            "LDFLAGS_USER=-L{0} {1}".format(
                self.spec["gettext"].prefix.lib, self.spec["gettext"].libs.link_flags
            )
        ]
        return targets

    def install(self, spec, prefix):
        make("prefix={0}".format(prefix), "install")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"^dos2unix\s+([\d\.]+)", output)
        return match.group(1) if match else None
