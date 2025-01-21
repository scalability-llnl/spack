# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScuttle(RPackage):
    """Single-Cell RNA-Seq Analysis Utilities.

    Provides basic utility functions for performing single-cell analyses,
    focusing on simple normalization, quality control and data transformations.
    Also provides some helper functions to assist development of other
    packages."""

    bioc = "scuttle"

    version("1.16.0", commit="ca4d5bd5ed1816015ec3e7a509afcb9a8bd1da33")
    version("1.14.0", commit="7e2bcaeb921a40a254f3f9276be1eb144d88266f")
    version("1.12.0", commit="94dd0660eb6c217abd130c25a0e14cdb97a30103")
    version("1.10.0", commit="02e864cb80414f71bb312cdf6d68e0036326e10b")
    version("1.8.0", commit="dabf6b95e478d599557ebbed03edd44031fd6b78")
    version("1.6.3", commit="df23680da9fa4d685df77e4561467f491c850b50")
    version("1.6.2", commit="afdfc555151d84cc332757b4ec0b97cb7f39d2d5")
    version("1.4.0", commit="b335263dd56bb859b5dd3ea27ee00dffa0215313")
    version("1.0.4", commit="a827e2759d80e6c3510e2f8fd4bd680274206d9f")

    depends_on("cxx", type="build")  # generated

    depends_on("r-singlecellexperiment", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-delayedarray", type=("build", "run"))
    depends_on("r-delayedmatrixstats", type=("build", "run"))
    depends_on("r-beachmat", type=("build", "run"))
