# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graphmap(MakefilePackage):
    """A highly sensitive and accurate mapper for long, error-prone reads"""

    homepage = "https://github.com/isovic/graphmap"
    git = "https://github.com/isovic/graphmap.git"

    license("MIT")

    version("0.3.0", commit="eb8c75d68b03be95464318afa69b645a59f8f6b7")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter("Makefile")
        makefile.filter("/usr/bin/graphmap", prefix.bin.graphmap)
        if self.spec.target.family == "aarch64":
            makefile.filter("-m64", "")

    def build(self, spec, prefix):
        make("modules")
        make()
