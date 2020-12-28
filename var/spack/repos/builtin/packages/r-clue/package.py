# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClue(RPackage):
    """clue: Cluster Ensembles"""

    homepage = "https://cloud.r-project.org/package=clue"
    url      = "https://cloud.r-project.org/src/contrib/clue_0.3-57.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/clue"

    version('0.3-57', sha256='6e369d07b464a9624209a06b5078bf988f01f7963076e946649d76aea0622d17')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
