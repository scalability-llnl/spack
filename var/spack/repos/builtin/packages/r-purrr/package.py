# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPurrr(RPackage):
    """A complete and consistent functional programming toolkit for R."""

    homepage = "http://purrr.tidyverse.org/"
    url      = "https://cloud.r-project.org/src/contrib/purrr_0.2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/purrr"

    version('0.3.4', sha256='23ebc93bc9aed9e7575e8eb9683ff4acc0270ef7d6436cc2ef4236a9734840b2')
    version('0.3.2', sha256='27c74dd9e4f6f14bf442473df22bcafc068822f7f138f0870326532f143a9a31')
    version('0.3.1', sha256='c2a3c9901192efd8a04976676f84885a005db88deb1432e4750900c7b3b7883b')
    version('0.2.4', sha256='ed8d0f69d29b95c2289ae52be08a0e65f8171abb6d2587de7b57328bf3b2eb71')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.3.3:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-rlang@0.3.1:', type=('build', 'run'))
    depends_on('r-tibble', when='@:0.2.9', type=('build', 'run'))
