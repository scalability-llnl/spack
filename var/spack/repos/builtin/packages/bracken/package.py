# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Bracken(Package):
    """Bracken (Bayesian Reestimation of Abundance with KrakEN) is a highly
    accurate statistical method that computes the abundance of species in DNA
    sequences from a metagenomics sample."""

    homepage = "https://ccb.jhu.edu/software/bracken"
    url = "https://github.com/jenniferlu717/Bracken/archive/v2.7.tar.gz"

    license("GPL-3.0-only")

    version("2.9", sha256="b8fd43fc396a2184d9351fb4a459f95ae9bb5865b195a18e22436f643044c788")
    version("2.8", sha256="b0c8a803cc020b7d1cbca47b53e71e874d9688b836911e4a4b71b0e4b826b61a")
    version("2.7", sha256="1795ecd9f9e5582f37549795ba68854780936110a2f6f285c3e626d448cd1532")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type="run")
    depends_on("kraken2", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin.src)
        # installer builds kmer2read_distr in src
        chmod = which("chmod")
        chmod("+x", "./install_bracken.sh")
        installer = Executable("./install_bracken.sh")
        installer(self.stage.source_path)
        # move main scripts to bin
        install("bracken", prefix.bin)
        install("bracken-build", prefix.bin)
        install("./src/kmer2read_distr", prefix.bin)
        install("./analysis_scripts/combine_bracken_outputs.py", prefix.bin)
        chmod("+x", join_path(prefix.bin, "combine_bracken_outputs.py"))
        # move scripts to src and create symlinks
        files = ("est_abundance.py", "generate_kmer_distribution.py")
        for file in files:
            filepath = join_path("./src", file)
            if os.path.isfile(filepath):
                install(filepath, prefix.bin.src)
                symlink(join_path(prefix.bin.src, file), join_path(prefix.bin, file))
