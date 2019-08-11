# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVegan(RPackage):
    """Ordination methods, diversity analysis and other functions for
    community and vegetation ecologists."""

    homepage = "https://github.com/vegandevs/vegan"
    url      = "https://cloud.r-project.org/src/contrib/vegan_2.4-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vegan"

    version('2.5-5', sha256='876b5266f29f3034fed881020d16f476e62d145a00cb450a1a213e019e056971')
    version('2.5-4', sha256='5116a440111fca49b5f95cfe888b180ff29a112e6301d5e2ac5cae0e628493e0')
    version('2.4-3', 'db17d4c4b9a4d421246abd5b36b00fec')

    depends_on('r@3.4:', type=('build', 'run'))
    depends_on('r-permute@0.9-0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
