# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMinfi(RPackage):
    """Analyze Illumina Infinium DNA methylation arrays.

    Tools to analyze & visualize Illumina Infinium methylation arrays."""

    bioc = "minfi"

    version("1.46.0", commit="1d063178fb27d577c260f8b7626b982c9a6585cc")
    version("1.44.0", commit="7c89fefc2e174d43ed9891b3f30b51ee19e916a6")
    version("1.42.0", commit="30fc7059460a9ec0be734fc26e608426ca9f5614")
    version("1.40.0", commit="17fa2b5d6cdbef6cbfb690242bd3f660731431f1")
    version("1.36.0", commit="94301da343226be7cd878c2a6c1bb529564785d6")
    version("1.30.0", commit="a4c28e9388fe3b35e7d21a9669e39250ed6dcbcd")
    version("1.28.4", commit="b5125b2f3e05d37d519eeb6fd44a60efdad388e7")
    version("1.26.2", commit="ebb07b728b2453998d46e4e53d4fbf873e8e81fc")
    version("1.24.0", commit="a4df428588ea86a1c79ddba76132014f0a39644e")
    version("1.22.1", commit="b2faf84bcbb291e32d470a0e029450093527545b")

    depends_on("r-biocgenerics@0.15.3:", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-summarizedexperiment@1.1.6:", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-bumphunter@1.1.9:", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-biobase@2.33.2:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-beanplot", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-nor1mix", type=("build", "run"))
    depends_on("r-siggenes", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-preprocesscore", type=("build", "run"))
    depends_on("r-illuminaio", type=("build", "run"))
    depends_on("r-illuminaio@0.23.2:", type=("build", "run"), when="@1.28.4:")
    depends_on("r-delayedmatrixstats", type=("build", "run"), when="@1.26.2:")
    depends_on("r-delayedmatrixstats@1.3.4:", type=("build", "run"), when="@1.28.4:")
    depends_on("r-mclust", type=("build", "run"))
    depends_on("r-genefilter", type=("build", "run"))
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-reshape", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-quadprog", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-geoquery", type=("build", "run"))
    depends_on("r-delayedarray@0.5.23:", type=("build", "run"), when="@1.26.2:")
    depends_on("r-delayedarray@0.7.38:", type=("build", "run"), when="@1.28.4:")
    depends_on("r-delayedarray@0.9.8:", type=("build", "run"), when="@1.30.0:")
    depends_on("r-delayedarray@0.15.16:", type=("build", "run"), when="@1.36.0:")
    depends_on("r-hdf5array", type=("build", "run"), when="@1.26.2:")
    depends_on("r-biocparallel", type=("build", "run"), when="@1.26.2:")

    depends_on("r-matrixstats@0.50.0:", type=("build", "run"), when="@:1.30.0")
