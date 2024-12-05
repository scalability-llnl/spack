# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tabix(MakefilePackage):
    """Generic indexer for TAB-delimited genome position files"""

    homepage = "https://github.com/samtools/tabix"
    git = "https://github.com/samtools/tabix.git"

    version("2013-12-16", commit="1ae158ac79b459f5feeed7490c67519b14ce9f35")

    depends_on("c", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("zlib-api", type="link")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man.man1)
        install("tabix", prefix.bin)
        install("bgzip", prefix.bin)
        install("tabix.py", prefix.bin)
        install("tabix.1", prefix.share.man.man1)
        install("tabix.tex", prefix.share)
        install("TabixReader.java", prefix.bin)
        install("libtabix.a", prefix.lib)
        install_tree("perl", prefix.perl)
        install_tree("python", prefix.python)
