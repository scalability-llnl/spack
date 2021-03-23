# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpadesCore(RPackage):
    """Utilities for Developing and Running Spatially Explicit Discrete Event Models

    Provides the core framework for a discrete event system (DES) to implement
    acomplete data-to-decisions, reproducible workflow. The core DES components
    facilitate modularity, and easily enable the user to include additional
    functionality by running user-built modules. Includes conditional scheduling,
    restart after interruption, packaging of reusable modules, tools for
    developing arbitrary automated workflows, automated interweaving of modules
    of different temporal resolution, and tools for visualizing and understanding
    the DES project."""

    homepage = "https://spades-core.predictiveecology.org/"
    url      = "https://cloud.r-project.org/src/contrib/SpaDES.core_1.0.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/SpaDES.core"

    maintainers = ['dorton21']

    version('1.0.5', sha256='c8b18cb5f932ea57f3cb3c7f2a302cbe7e06c875da7cd3928300d6003602f0a6')

    depends_on('r@3.6:', type=('build', 'run'))
    depends_on('r-quickplot@0.1.4:', type=('build', 'run'))
    depends_on('r-reproducible@1.2.1.9007:', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-data-table@1.10.4:', type=('build', 'run'))
    depends_on('r-fastdigest', type=('build', 'run'))
    depends_on('r-igraph@1.0.1:', type=('build', 'run'))
    depends_on('r-qs@0.21.1:', type=('build', 'run'))
    depends_on('r-raster@2.5-8:', type=('build', 'run'))
    depends_on('r-require@0.0.7:', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
