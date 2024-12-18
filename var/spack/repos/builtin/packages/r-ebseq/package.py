# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REbseq(RPackage):
    """An R package for gene and isoform differential expression analysis of RNA-seq data.

    R/EBSeq is an R package for identifying genes and isoforms differentially
    expressed (DE) across two or more biological conditions in an RNA-seq
    experiment. Details can be found in Leng et al., 2013. It provides the syntax
    required for identifying DE genes and isoforms in a two-group RNA-seq
    experiment as well for identifying DE genes across more than two conditions
    (the commands for identifying DE isoforms across more than two conditions
    are the same as those required for gene-level analysis)."""

    maintainers("pabloaledo")

    bioc = "EBSeq"

    version("2.0.0", commit="f1d4e4419988ab98540739c9349559fd437cb59f")
    version("1.40.0", commit="7d1d2a2b4ea0df8cddfb5e57d6431f3948c5c4ca")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-bh", type=("build", "run"))
    depends_on("r-blockmodeling", type=("build", "run"))
    depends_on("r-gplots", type=("build", "run"))
    depends_on("r-rcppeigen@0.3.2.9.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.11:", type=("build", "run"))
    depends_on("r-testthat", type=("build", "run"))
