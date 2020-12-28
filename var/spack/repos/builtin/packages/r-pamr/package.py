# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPamr(RPackage):
    """Some functions for sample classification in microarrays."""

    homepage = "https://cloud.r-project.org/package=pamr"
    url      = "https://cloud.r-project.org/src/contrib/pamr_1.55.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pamr"

    version('1.56.1', sha256='d0e527f2336ee4beee91eefb2a8f0dfa96413d9b5a5841d6fc7ff821e67c9779')
    version('1.55', sha256='ed910194937a6097ec79234d84777856fd520b111a7c79f7c86dc607169cc3c3')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
