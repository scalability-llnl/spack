# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BioconductorEbseq(RPackage):
    """An R package for gene and isoform differential expression analysis of RNA-seq data.

    R/EBSeq is an R package for identifying genes and isoforms differentially
    expressed (DE) across two or more biological conditions in an RNA-seq
    experiment. Details can be found in Leng et al., 2013. It provides the syntax
    required for identifying DE genes and isoforms in a two-group RNA-seq
    experiment as well for identifying DE genes across more than two conditions
    (the commands for identifying DE isoforms across more than two conditions
    are the same as those required for gene-level analysis)."""

    homepage = "https://www.biostat.wisc.edu/~kendzior/EBSEQ/"
    url = "https://bioconductor.org/packages/release/bioc/src/contrib/EBSeq_1.40.0.tar.gz"
    maintainers("pabloaledo")

    bioc = "ebseq"

    version(
        "1.40.0",
        sha256="a5d3a88743d61062c6d68a426b19c53a4afd2fa216abc884d42c187780994378",
        deprecated=True,
    )

    depends_on("r-blockmodeling")
    depends_on("r-gplots")
    depends_on("r-testthat")
