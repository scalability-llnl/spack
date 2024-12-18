# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fermikit(MakefilePackage):
    """De novo assembly based variant calling pipeline for Illumina short
    reads"""

    homepage = "https://github.com/lh3/fermikit"
    git = "https://github.com/lh3/fermikit.git"

    version("2017-11-7", commit="bf9c7112221577ba110665bddca8f1987250bdc7", submodules=True)

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("sse2neon", when="target=aarch64:")

    patch("ksw_for_aarch64.patch", when="target=aarch64:")

    def install(self, spec, prefix):
        install_tree("fermi.kit", prefix.bin)
