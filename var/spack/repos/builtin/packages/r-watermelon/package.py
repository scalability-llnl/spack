# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWatermelon(RPackage):
    """Illumina 450 methylation array normalization and metrics."""

    homepage = "https://bioconductor.org/packages/release/bioc/html/wateRmelon.html"
    git      = "https://git.bioconductor.org/packages/wateRmelon"

    version('1.30.0', commit='66d7579fe49206d965832288df7937c3d43ed578')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-methylumi', type=('build', 'run'))
    depends_on('r-lumi', type=('build', 'run'))
    depends_on('r-roc', type=('build', 'run'))
    depends_on('r-illuminahumanmethylation450kanno-ilmn12-hg19', type=('build', 'run'))
    depends_on('r-illuminaio', type=('build', 'run'))
