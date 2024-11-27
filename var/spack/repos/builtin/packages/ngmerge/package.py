# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ngmerge(MakefilePackage):
    """Merging paired-end reads and removing adapters."""

    homepage = "https://github.com/jsh58/NGmerge"
    url = "https://github.com/jsh58/NGmerge/archive/v0.3.tar.gz"

    license("MIT")

    version("0.3", sha256="5928f727feebd0d1bcdbee0e631ba06fbe9ce88328bd58b6c8bf4e54cc742ac3")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("NGmerge", prefix.bin)
