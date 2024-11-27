# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCorhmm(RPackage):
    """Hidden Markov Models of Character Evolution.

    Fits hidden Markov models of discrete character evolution which allow
    different transition rate classes on different portions of a phylogeny.
    Beaulieu et al (2013) <doi:10.1093/sysbio/syt034>."""

    cran = "corHMM"

    version("2.8", sha256="d6e46641f5b2b15720c8bb6c51d715220519dd8a6ba44171d13ef75bfa2eb6df")
    version("2.7", sha256="0d54ba0f6b3f884343bcc26919d8febc05efb0b739cb962d3072ca0bc0ce270a")
    version("2.6", sha256="726de9707ede8ef447915171a3abe1003a0e42fe8e17eb440442cac9adf8cdcf")
    version("1.22", sha256="d262fa1183eab32087afb70f1789fabae6fb49bec01d627974c54a088a48b10d")

    depends_on("r-ape", type=("build", "run"))
    depends_on("r-nloptr", type=("build", "run"))
    depends_on("r-gensa", type=("build", "run"))
    depends_on("r-expm", type=("build", "run"))
    depends_on("r-numderiv", type=("build", "run"))
    depends_on("r-corpcor", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"), when="@2.6:")
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-phangorn", type=("build", "run"))
    depends_on("r-viridis", type=("build", "run"), when="@2.6:")
    depends_on("r-rmpfr", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"), when="@2.6:")
    depends_on("r-phytools", type=("build", "run"), when="@2.6:")
