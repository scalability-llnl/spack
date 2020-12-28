# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLoo(RPackage):
    """loo: Efficient Leave-One-Out Cross-Validation and WAIC for
       BayesianModels"""

    homepage = "https://mc-stan.org/loo"
    url      = "https://cloud.r-project.org/src/contrib/loo_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/loo"

    version('2.3.1', sha256='d98de21b71d9d9386131ae5ba4da051362c3ad39e0305af4f33d830f299ae08b')
    version('2.1.0', sha256='1bf4a1ef85d151577ff96d4cf2a29c9ef24370b0b1eb08c70dcf45884350e87d')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-checkmate', type=('build', 'run'))
    depends_on('r-matrixstats@0.52:', type=('build', 'run'))
    depends_on('pandoc@1.12.3:')
