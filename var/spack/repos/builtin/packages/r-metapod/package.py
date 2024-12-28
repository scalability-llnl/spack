# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMetapod(RPackage):
    """Meta-Analyses on P-Values of Differential Analyses.

    Implements a variety of methods for combining p-values in differential
    analyses of genome-scale datasets. Functions can combine p-values across
    different tests in the same analysis (e.g., genomic windows in ChIP-seq,
    exons in RNA-seq) or for corresponding tests across separate analyses
    (e.g., replicated comparisons, effect of different treatment conditions).
    Support is provided for handling log-transformed input p-values, missing
    values and weighting where appropriate."""

    bioc = "metapod"

    version("1.14.0", commit="bf476aa42ca9629f1e6e9596cc99370af479625d")
    version("1.12.0", commit="4f07cb9abcb8b0014a151425ea830e6d48929155")
    version("1.10.1", commit="88465ba68da00c656131f51001889f021da30baf")
    version("1.8.0", commit="6ac6999182d581ed579d2f7535e838b084f67b8d")
    version("1.6.0", commit="cfeaa959f5c6b2119df270f40af9c3ea718c4b00")
    version("1.4.0", commit="e71c2072e5b39f74599e279b28f4da7923b515fb")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp", type=("build", "run"))
