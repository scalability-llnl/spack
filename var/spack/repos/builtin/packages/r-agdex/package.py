# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAgdex(RPackage):
    """Agreement of Differential Expression Analysis.

       A tool to evaluate agreement of differential expression for cross-
       species genomics"""

    homepage = "https://bioconductor.org/packages/AGDEX"
    git      = "https://git.bioconductor.org/packages/AGDEX.git"

    version('1.32.0', commit='254ad2c876ab9ac48c3c3b395160dccabc084acf')
    version('1.30.0', commit='d6cc21ed7e11e6644399495fa5f8b36368625d4b')
    version('1.28.0', commit='7d78ee424485018b73cd019ceaed7a2ed53adf3f')
    version('1.26.0', commit='260bc641111770176707d4d43e67b5877bf5eb82')
    version('1.24.0', commit='29c6bcfa6919a5c6d8bcb36b44e75145a60ce7b5')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
