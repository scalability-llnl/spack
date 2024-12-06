# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDss(RPackage):
    """Dispersion shrinkage for sequencing data.

    DSS is an R library performing differntial analysis for count-based
    sequencing data. It detectes differentially expressed genes (DEGs) from
    RNA-seq, and differentially methylated loci or regions (DML/DMRs) from
    bisulfite sequencing (BS-seq). The core of DSS is a new dispersion
    shrinkage method for estimating the dispersion parameter from Gamma-Poisson
    or Beta-Binomial distributions."""

    bioc = "DSS"

    version("2.48.0", commit="03ceee2656e57b717e4fd7f22ff389f118421ae1")
    version("2.46.0", commit="debfbac4bc741961ba57915d4f2d98534f02cc21")
    version("2.44.0", commit="b9f44106f139c93564dfb4afab50555d24a657ba")
    version("2.42.0", commit="33e87450fbb64bb3e321688ff613e83cd40efe48")
    version("2.38.0", commit="82e65b92e6e227f1f99620362db8b03059e07e98")
    version("2.36.0", commit="841c7ed72a138a458ee2df52336050dbe581e727")
    version("2.34.0", commit="f9819c7d7927c8e6d9963632cdeab36c8c22caa8")
    version("2.32.0", commit="ffb502d20810a873c2376199d44adedf7c83912d")

    depends_on("c", type="build")  # generated

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.44.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-biocparallel", type=("build", "run"), when="@2.36.0:")
    depends_on("r-bsseq", type=("build", "run"))

    depends_on("r-delayedarray", type=("build", "run"), when="@2.36.0:2.42.0")
    depends_on("r-matrixstats", type=("build", "run"), when="@2.44.0")
