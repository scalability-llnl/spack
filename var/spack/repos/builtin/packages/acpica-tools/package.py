# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AcpicaTools(MakefilePackage):
    """Debian packaging for the ACPICA user space tools"""

    homepage = "https://github.com/ahs3/acpica-tools"
    url = "https://github.com/ahs3/acpica-tools/archive/upstream/20200528.tar.gz"

    version("20200528", sha256="07cd3e370b695ab787d25a7165e37eb7b150dca7908f047a6a6486d216cf05a8")
    version("20200430", sha256="e3118583bf6e4bb4745d642a863cce1b4fcfdf67558e4ae53df367b7e26b89ac")

    depends_on("c", type="build")  # generated

    depends_on("flex", type="build")
    depends_on("bison", type="build")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
