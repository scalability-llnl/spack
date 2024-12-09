# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTfbstools(RPackage):
    """Software Package for Transcription Factor Binding Site (TFBS) Analysis.

    TFBSTools is a package for the analysis and manipulation of
    transcription factor binding sites. It includes matrices conversion
    between Position Frequency Matirx (PFM), Position Weight Matirx (PWM)
    and Information Content Matrix (ICM). It can also scan putative TFBS
    from sequence/alignment, query JASPAR database and provides a wrapper of
    de novo motif discovery software."""

    bioc = "TFBSTools"

    version("1.38.0", commit="2ce17166b6f73b5093acec2a3dde33b6bcfa56bc")
    version("1.36.0", commit="3358c89227a4d2e237ee5f8c532f468460a16ee2")
    version("1.34.0", commit="7f8d0cb58a527a5d7ba94a773279f13aedca6ec7")
    version("1.32.0", commit="235505626b910de29156a07e1f990daa3b5d57d9")
    version("1.28.0", commit="15e7cf76f39ee3280a27284d58f7adef1c33f193")
    version("1.22.0", commit="613d3567fd662b65269bd200c5aa5f87ac6a4612")
    version("1.20.0", commit="74035fc6beb1af82f171c11ef2b0a8817714c5bc")
    version("1.18.0", commit="17e12b9f3dcb9059d414307ec0bc23ed1ee33294")
    version("1.16.0", commit="565436a5a674d4dea7279e796a20c5bd2034f65a")
    version("1.14.2", commit="e429fdefb6f7ee4585dd2a8ca3d0ced7a5bed4ff")

    depends_on("c", type="build")  # generated

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r-biobase@2.28:", type=("build", "run"))
    depends_on("r-biostrings@2.36.4:", type=("build", "run"))
    depends_on("r-biocgenerics@0.14.0:", type=("build", "run"))
    depends_on("r-biocparallel@1.2.21:", type=("build", "run"))
    depends_on("r-bsgenome@1.36.3:", type=("build", "run"))
    depends_on("r-catools@1.17.1:", type=("build", "run"))
    depends_on("r-cner@1.4.0:", type=("build", "run"))
    depends_on("r-dirichletmultinomial@1.10.0:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.6.1:", type=("build", "run"))
    depends_on("r-genomicranges@1.20.6:", type=("build", "run"))
    depends_on("r-gtools@3.5.0:", type=("build", "run"))
    depends_on("r-iranges@2.2.7:", type=("build", "run"))
    depends_on("r-dbi@0.6:", type=("build", "run"))
    depends_on("r-rsqlite@1.0.0:", type=("build", "run"))
    depends_on("r-rtracklayer@1.28.10:", type=("build", "run"))
    depends_on("r-seqlogo@1.34.0:", type=("build", "run"))
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-tfmpvalue@0.0.5:", type=("build", "run"))
    depends_on("r-xml@3.98-1.3:", type=("build", "run"))
    depends_on("r-xvector@0.8.0:", type=("build", "run"))
