# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sambamba(Package):
    """Sambamba: process your BAM data faster (bioinformatics)"""

    homepage = "https://lomereiter.github.io/sambamba/"
    git = "https://github.com/lomereiter/sambamba.git"

    license("GPL-2.0-only")

    version(
        "0.6.6", tag="v0.6.6", commit="63cfd5c7b3053e1f7045dec0b5a569f32ef73d06", submodules=True
    )

    depends_on("c", type="build")  # generated

    depends_on("ldc~shared", type=("build", "link"))
    depends_on("python", type="build")

    resource(name="undeaD", git="https://github.com/dlang/undeaD.git", tag="v1.0.7")

    patch("Makefile.patch")
    parallel = False

    def install(self, spec, prefix):
        make("sambamba-ldmd2-64")
        mkdirp(prefix.bin)
        for filename in ("build/sambamba", "build/sambamba.debug"):
            install(filename, prefix.bin)
