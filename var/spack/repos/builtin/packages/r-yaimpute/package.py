# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYaimpute(RPackage):
    """Performs nearest neighbor-based imputation using one or more
       alternative approaches to processing multivariate data
    """

    homepage = "https://cloud.r-project.org/package=yaImpute"
    url      = "https://cloud.r-project.org/src/contrib/yaImpute_1.0-32.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/yaImpute"

    version('1.0-32', sha256='08eee5d851b80aad9c7c80f9531aadd50d60e4b16b3a80657a50212269cd73ff')

    depends_on('r@3.0:', type=('build', 'run'))
