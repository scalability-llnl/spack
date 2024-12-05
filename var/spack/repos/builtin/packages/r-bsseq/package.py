# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBsseq(RPackage):
    """Analyze, manage and store bisulfite sequencing data.

    A collection of tools for analyzing and visualizing bisulfite sequencing
    data."""

    bioc = "bsseq"

    version("1.36.0", commit="5dd72c5a84e1fcc3389ab2a74f8ca14c399ac128")
    version("1.34.0", commit="98239c07d74e1362c7ba2a3bf4f6119830fc95dc")
    version("1.32.0", commit="a0c1eacbc479c57bd836e885e162c28bbe08e115")
    version("1.30.0", commit="7eb5223e9ee02fd08a52be56eaa9316a67c0d66b")
    version("1.26.0", commit="fae32292687625012a2938a48c93df55ad4257b5")
    version("1.24.4", commit="8fe7a035802055cf14783d2ab92af70c5d5800ed")
    version("1.22.0", commit="d4f7301dcd4a03431b0833302b5a79c6f1b186cc")
    version("1.20.0", commit="07e398bc38ba903881df9a5d0577cca15788e0cd")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.5:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-genomicranges@1.29.14:", type=("build", "run"))
    depends_on("r-genomicranges@1.33.6:", type=("build", "run"), when="@1.24.4:")
    depends_on("r-genomicranges@1.41.5:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-summarizedexperiment@1.9.18:", type=("build", "run"))
    depends_on("r-summarizedexperiment@1.17.4:", type=("build", "run"), when="@1.24.4:")
    depends_on("r-summarizedexperiment@1.19.5:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-iranges@2.11.16:", type=("build", "run"))
    depends_on("r-iranges@2.22.2:", type=("build", "run"), when="@1.24.4:")
    depends_on("r-iranges@2.23.9:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-gtools", type=("build", "run"))
    depends_on("r-data-table@1.11.8:", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-s4vectors@0.23.11:", type=("build", "run"), when="@1.22.0:")
    depends_on("r-s4vectors@0.25.14:", type=("build", "run"), when="@1.24.4:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-r-utils@2.0.0:", type=("build", "run"))
    depends_on("r-delayedmatrixstats@1.5.2:", type=("build", "run"))
    depends_on("r-permute", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-delayedarray@0.9.8:", type=("build", "run"))
    depends_on("r-delayedarray@0.15.16:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-bsgenome", type=("build", "run"))
    depends_on("r-biostrings", type=("build", "run"))
    depends_on("r-hdf5array@1.11.9:", type=("build", "run"))
    depends_on("r-hdf5array@1.15.19:", type=("build", "run"), when="@1.26.0:")
    depends_on("r-hdf5array@1.19.11:", type=("build", "run"), when="@1.30.0:")
    depends_on("r-rhdf5", type=("build", "run"))
    depends_on("r-beachmat", type=("build", "run"))
