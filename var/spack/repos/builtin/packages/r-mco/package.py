# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMco(RPackage):
    """Functions for multiple criteria optimization using genetic algorithms
       and related test problems"""

    homepage = "https://github.com/cran/mco"
    url      = "https://cloud.r-project.org/src/contrib/mco_1.0-15.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mco"

    version('1.0-15.1', sha256='3c13ebc8c1f1bfa18f3f95b3998c57fde5259876e92456b6c6d4c59bef07c193')
    version('1.0-15', sha256='a25e3effbb6dcae735fdbd6c0bfc775e9fbbcc00dc00076b69c53fe250627055')

    depends_on('r@3.0.0:', type=('build', 'run'))
