# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTximeta(RPackage):
    """Transcript Quantification Import with Automatic Metadata

    Transcript quantification import from Salmon and alevin with automatic
    attachment of transcript ranges and release information, and other associated
    metadata. De novo transcriptomes can be linked to the appropriate sources with
    linkedTxomes and shared for computational reproducibility."""

    bioc = "tximeta"

    version("1.20.0", commit="c9cf6d6a80ca5129b91d723867aca0aec12e8299")
    version("1.18.3", commit="3caed00397476cfe9c379f4bc5a361023fdd6ffa")
    version("1.18.0", commit="8f87d53bbd6f2d97821dd8f7fdd54624928f862d")

    depends_on("r", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-annotationhub", type=("build", "run"))
    depends_on("r-biocfilecache", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-ensembldb", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-genomicfeatures", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-r-utils", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tximport", type=("build", "run"))
