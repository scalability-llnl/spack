# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScdblfinder(RPackage):
    """The scDblFinder package gathers various methods for the detection and
    handling of doublets/multiplets in single-cell sequencing data (i.e.
    multiple cells captured within the same droplet or reaction volume). It
    includes methods formerly found in the scran package, the new fast and
    comprehensive scDblFinder method, and a reimplementation of the Amulet
    detection method for single-cell ATAC-seq."""

    bioc = "scDblFinder"

    license("GPL-3.0-only")

    version("1.14.0", commit="6191ed09b87d7c54809a721d1d6c50c0027cf0a9")
    version("1.12.0", commit="65a88be3a4ca98ccad0a1829a19652df1a3c94fd")
    version("1.10.0", commit="03512cad0cdfe3cddbef66ec5e330b53661eccfc")

    depends_on("r@4.0:", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-biocneighbors", type=("build", "run"))
    depends_on("r-biocsingular", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-singlecellexperiment", type=("build", "run"))
    depends_on("r-scran", type=("build", "run"))
    depends_on("r-scater", type=("build", "run"))
    depends_on("r-scuttle", type=("build", "run"))
    depends_on("r-bluster", type=("build", "run"))
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-xgboost", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))
    depends_on("r-rtracklayer", type=("build", "run"))
