# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dmidecode(MakefilePackage):
    """Dmidecode reports information about your system's hardware
    as described in your system BIOS according to the SMBIOS/DMI standard. ."""

    homepage = "https://github.com/mirror/dmidecode"
    url = "https://github.com/mirror/dmidecode/archive/dmidecode-3-2.tar.gz"

    license("GPL-2.0-or-later")

    version("3-2", sha256="489d840d076785617a432649603aafa6358327f4376694c062b69dfa359bcc2d")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("dmidecode", prefix.bin)
