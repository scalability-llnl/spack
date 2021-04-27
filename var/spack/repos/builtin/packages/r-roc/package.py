# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRoc(RPackage):
    """utilities for ROC, with microarray focus

    Provide utilities for ROC, with microarray focus."""

    homepage = "https://bioconductor.org/packages/release/bioc/html/ROC.html"
    git      = "https://git.bioconductor.org/packages/ROC"

    version('1.66.0', commit='62701ee41f48f99d15344127384fa032db69486f')
    version('1.62.0', commit='60250fdb091f6a938709b8a2cffe6442ee22a9a2')

    depends_on('r@1.9.0:', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
