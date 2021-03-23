# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpades(RPackage):
    """Develop and Run Spatially Explicit Discrete Event Simulation Models

    Metapackage for implementing a variety of event-based models, with a
    focus on spatially explicit models. These include raster-based,
    event-based, and agent-based models."""

    homepage = "http://spades.predictiveecology.org/"
    url      = "https://cloud.r-project.org/src/contrib/SpaDES_2.0.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/SpaDES"

    maintainers = ['dorton21']

    version('2.0.6', sha256='0fa59d1737c67abeb04eae894939bc4700f92d6c2cc2ec3489b4650720ede5a3')

    depends_on('r@3.6:', type=('build', 'run'))
    depends_on('r-quickplot', type=('build', 'run'))
    depends_on('r-reproducible@1.2.1.9007:', type=('build', 'run'))
    depends_on('r-spades-addins', type=('build', 'run'))
    depends_on('r-spades-core@1.0.4:', type=('build', 'run'))
    depends_on('r-spades-tools', type=('build', 'run'))
