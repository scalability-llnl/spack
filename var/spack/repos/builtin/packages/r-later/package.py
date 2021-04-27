# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLater(RPackage):
    """Utilities for Scheduling Functions to Execute Later with Event Loops

    Executes arbitrary R or C functions some time after the current time,
    after the R execution stack has emptied."""

    homepage = "https://github.com/r-lib/later"
    url      = "https://cloud.r-project.org/src/contrib/later_0.8.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/later"

    version('1.1.0.1', sha256='71baa7beae774a35a117e01d7b95698511c3cdc5eea36e29732ff1fe8f1436cd')
    version('0.8.0', sha256='6b2a28b43c619b2c7890840c62145cd3a34a7ed65b31207fdedde52efb00e521')

    depends_on('r-rcpp@0.12.9:', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
