# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGgforce(RPackage):
    """Accelerating 'ggplot2'

    The aim of 'ggplot2' is to aid in visual data investigations. This focus
    has led to a lack of facilities for composing specialised plots. 'ggforce'
    aims to be a collection of mainly new stats and geoms that fills this gap.
    All additional functionality is aimed to come through the official
    extension system so using 'ggforce' should be a stable experience."""

    homepage = "https://ggforce.data-imaginist.com"
    url      = "https://cloud.r-project.org/src/contrib/ggforce_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggforce"

    version('0.3.2', sha256='4cce8acb60ce06af44c1c76bbacd7de129eed9b51ed6a85e03a9bf55b0eff4d2')
    version('0.3.1', sha256='a05271da9b226c12ae5fe6bc6eddb9ad7bfe19e1737e2bfcd6d7a89631332211')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.2:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-tweenr@0.1.5:', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-polyclip', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
