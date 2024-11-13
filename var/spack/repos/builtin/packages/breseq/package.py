# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Breseq(AutotoolsPackage):
    """breseq is a computational pipeline for finding mutations relative to
    a reference sequence in short-read DNA re-sequencing data for haploid
    microbial-sized genomes."""

    homepage = "https://barricklab.org/breseq"
    url = "https://github.com/barricklab/breseq/archive/v0.31.1.tar.gz"

    license("GPL-2.0-or-later")

    version("0.38.1", sha256="2b5d0aa9c751881c3ee31c0384953156b848b80d2d2d9c451763d74da0465902")
    version("0.33.2", sha256="c698d2d25cc7ed251ff916343a8c04f79b5540281288cb7c955f458255ac21de")
    version("0.33.1", sha256="e24a50e254ad026c519747313b9e42bbeb32bd766a6a06ed369bd5b9dc50e84d")
    version("0.31.1", sha256="ffc8a7f40a5ad918234e465e9d4cdf74be02fd29091b13720c2cab1dc238cf5c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api", type="link")

    depends_on("bedtools2", type="run")
    depends_on("r", type="run")

    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.3")

    def setup_build_environment(self, env):
        env.set("LDFLAGS", "-L{0}".format(self.spec["zlib-api"].prefix.lib))
        env.set("CFLAGS", "-I{0}".format(self.spec["zlib-api"].prefix.include))
