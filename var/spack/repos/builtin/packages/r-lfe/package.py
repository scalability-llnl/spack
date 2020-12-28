# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLfe(AutotoolsPackage):
    """Transforms away factors with many levels prior to doing an OLS"""

    homepage = "https://cloud.r-project.org/package=lfe"
    url      = "https://cloud.r-project.org/src/contrib/lfe_2.8-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lfe"

    version('2.8-5', sha256='fd80c573d334594db933ff38f67bd4c9f899aaf648c3bd68f19477a0059723c2')
    version('2.8-4', sha256='ee5f6e312214aa73e285ae84a6bdf49ba10e830f1a68ffded2fea2e532f2cd6a')

    depends_on('r@2.15.2:', type=('build', 'run'))
    depends_on('r-matrix@1.1-2:', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
