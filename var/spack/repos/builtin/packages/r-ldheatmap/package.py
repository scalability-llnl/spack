# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLdheatmap(RPackage):
    """LDheatmap: Graphical Display of Pairwise Linkage Disequilibria Between
       SNPs"""

    homepage = "https://sfustatgen.github.io/LDheatmap/"
    url      = "https://cloud.r-project.org/src/contrib/LDheatmap_0.99-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/LDheatmap"

    version('0.99-7', sha256='aca54c839a424506d8be7153bf03b32026aeefe7ed38f534e8e19708e34212e4')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-genetics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-snpstats', type=('build', 'run'))
