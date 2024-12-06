# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAlpine(RPackage):
    """alpine.

    Fragment sequence bias modeling and correction for RNA-seq transcript
    abundance estimation."""

    bioc = "alpine"

    version("1.26.0", commit="1e317dbf2973eb4b6a3ffbf52bc0faacec76a616")
    version("1.24.0", commit="7e734d49881761cafaacea096ce757531b6bd522")
    version("1.22.0", commit="6107a82962f07e0434e93f261cd375eaaa171d91")
    version("1.20.0", commit="9348ef14128aa6be10cca1987736ddbc385df7e9")
    version("1.16.0", commit="aee397774ac6cd17ad45dc05be14c526647f3c13")
    version("1.10.0", commit="bf22597eb2c6c6aaa26900ed4ece96ce7256e77c")
    version("1.8.0", commit="ddaa0b4517f0909460aa1bd33c8e43dc6c8d23d4")
    version("1.6.0", commit="ea55fcb3cedb5caa20d8264bb29a4975041f5274")
    version("1.4.0", commit="c85beb208fd6bfc0a61a483a98498b589640f946")
    version("1.2.0", commit="896872e6071769e1ac2cf786974edb8b875c45eb")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-genomicalignments", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-genomicfeatures", type=("build", "run"))
    depends_on("r-speedglm", type=("build", "run"))
    depends_on("r-graph", type=("build", "run"))
    depends_on("r-rbgl", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
