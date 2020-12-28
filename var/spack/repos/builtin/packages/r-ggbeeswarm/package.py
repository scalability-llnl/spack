# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgbeeswarm(RPackage):
    """ggbeeswarm: Categorical Scatter (Violin Point) Plots"""

    homepage = "https://github.com/eclarke/ggbeeswarm"
    url      = "https://cloud.r-project.org/src/contrib/ggbeeswarm_0.6.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggbeeswarm"

    version('0.6.0', sha256='bbac8552f67ff1945180fbcda83f7f1c47908f27ba4e84921a39c45d6e123333')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-beeswarm', type=('build', 'run'))
    depends_on('r-ggplot2@2.0:', type=('build', 'run'))
    depends_on('r-vipor', type=('build', 'run'))
