# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgforce(RPackage):
    """ggforce: Accelerating 'ggplot2'"""

    homepage = "https://ggforce.data-imaginist.com"
    url      = "https://cloud.r-project.org/src/contrib/ggforce_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggforce"

    version('0.3.1', sha256='a05271da9b226c12ae5fe6bc6eddb9ad7bfe19e1737e2bfcd6d7a89631332211')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-polyclip', type=('build', 'run'))
    depends_on('r-rcpp@0.12.2:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-tidyselect', type=('build', 'run'))
    depends_on('r-tweenr@0.1.5:', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
