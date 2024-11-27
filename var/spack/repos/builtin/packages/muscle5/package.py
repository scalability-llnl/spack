# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muscle5(MakefilePackage):
    """MUSCLE is widely-used software for making multiple alignments of
    biological sequences.
    """

    homepage = "https://drive5.com/muscle5/"
    url = "https://github.com/rcedgar/muscle/archive/refs/tags/5.1.0.tar.gz"

    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("5.1.0", sha256="2bba8b06e3ccabf6465fa26f459763b2029d7e7b9596881063e3aaba60d9e87d")

    depends_on("cxx", type="build")  # generated

    depends_on("sed", type="build")

    build_directory = "src"

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("src/Linux/muscle", prefix.bin)
