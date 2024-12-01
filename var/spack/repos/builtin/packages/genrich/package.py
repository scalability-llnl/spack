# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Genrich(MakefilePackage):
    """Genrich is a peak-caller for genomic enrichment assays."""

    homepage = "https://github.com/jsh58/Genrich"
    url = "https://github.com/jsh58/Genrich/archive/v0.6.tar.gz"

    license("MIT")

    version("0.6.1", sha256="2c70239e1caf33519b9e99142470bb4dd2f4c69e71f68cee33d6d6a1032d0e33")
    version("0.6", sha256="4c87aca8b7789f28b0c5c2c0ccea75668f19fa6a4cb38cd3c06d80ffd98d396f")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("Genrich", prefix.bin)
