# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForcats(RPackage):
    """Helpers for reordering factor levels (including moving specified levels
       to front, ordering by first appearance, reversing, and randomly
       shuffling), and tools for modifying factor levels (including collapsing
       rare levels into other, 'anonymising', and manually 'recoding')."""

    homepage = "http://forcats.tidyverse.org/"
    url      = "https://cloud.r-project.org/src/contrib/forcats_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/forcats"

    version('0.4.0', sha256='7c83cb576aa6fe1379d7506dcc332f7560068b2025f9e3ab5cd0a5f28780d2b2')
    version('0.3.0', sha256='95814610ec18b8a8830eba63751954387f9d21400d6ab40394ed0ff22c0cb657')
    version('0.2.0', sha256='b5bce370422d4c0ec9509249ae645373949bfbe9217cdf50dce2bfbdad9f7cd7')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-ellipsis', when='@0.4.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.4.0:', type=('build', 'run'))
