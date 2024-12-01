# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muse(MakefilePackage):
    """Somatic point mutation caller."""

    homepage = "https://bioinformatics.mdanderson.org/main/MuSE"
    url = "https://github.com/danielfan/MuSE/archive/v1.0-rc.tar.gz"

    license("GPL-2.0-or-later")

    version("1.0-rc", sha256="b48b8be0044a2249bdc0b625fe0192c65089c598bbd1b1142902dfa81e804023")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("MuSE", prefix.bin.MuSE)
