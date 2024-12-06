# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Angsd(MakefilePackage):
    """Angsd is a program for analysing NGS data.

    The software can handle a number of different input types from mapped
    reads to imputed genotype probabilities. Most methods take genotype
    uncertainty into account instead of basing the analysis on called
    genotypes. This is especially useful for low and medium depth data.
    """

    homepage = "https://github.com/ANGSD/angsd"
    url = "https://github.com/ANGSD/angsd/archive/0.935.tar.gz"

    version("0.935", sha256="15000281330fa59ddf745cb84eeaa653acf6da34a4ac6c3df7c5835d1d01ba16")
    version("0.933", sha256="2f992325dc08fa25ac525d9300ef6bd61808e74c521b4cc72a2ce00d98f402bb")
    version("0.921", sha256="8892d279ce1804f9e17fe2fc65a47e5498e78fc1c1cb84d2ca2527fd5c198772")
    version("0.919", sha256="c2ea718ca5a5427109f4c3415e963dcb4da9afa1b856034e25c59c003d21822a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("r", default=True, description="Enable R dependency")

    depends_on("htslib")
    conflicts("^htslib@1.6:", when="@0.919")

    depends_on("zlib-api")
    depends_on("lzma")
    depends_on("curl")

    depends_on("r", type="run", when="+r")

    def setup_run_environment(self, env):
        env.set("R_LIBS", self.prefix.R)

    def install(self, spec, prefix):
        binaries = ["angsd", "misc/realSFS", "misc/thetaStat"]

        mkdirp(prefix.bin)

        for b in binaries:
            install(b, join_path(prefix.bin))

        install_tree("R", prefix.R)
        install_tree("RES", prefix.RES)
        install_tree("scripts", prefix.scripts)
