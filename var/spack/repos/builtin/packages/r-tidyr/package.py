# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidyr(RPackage):
    """An evolution of 'reshape2'. It's designed specifically for data tidying
    (not general reshaping or aggregating) and works well with 'dplyr' data
    pipelines."""

    homepage = "https://github.com/hadley/tidyr"
    url      = "https://cloud.r-project.org/src/contrib/tidyr_0.7.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tidyr"

    version('0.8.3', sha256='a18f54ec35124110058ab23f7e0a3c037a8d50f0405520cf5cc5443ec022cc37')
    version('0.8.2', sha256='99a508d0539390364789c5f4835b36c4a383927f0ec1648e2a4636c1cc6e490f')
    version('0.7.2', sha256='062cea2e2b57fffd500e4ce31cba6d593e65684fc0897ea49ea38d257c76009c')
    version('0.5.1', sha256='dbab642ac7231cbfe3e2a0d4553fb4ffb3699c6d6b432be2bb5812dfbbdbdace')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-tidyselect@0.2.5:', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
