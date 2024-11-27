# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mefit(Package):
    """This pipeline will merge overlapping paired-end reads, calculate
    merge statistics, and filter reads for quality."""

    homepage = "https://github.com/nisheth/MeFiT"
    git = "https://github.com/nisheth/MeFiT.git"

    version("1.0", commit="0733326d8917570bbf70ff5c0f710bf66c13db09")

    depends_on("py-numpy")
    depends_on("py-htseq")
    depends_on("jellyfish")
    depends_on("casper %gcc@4.8.5")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
