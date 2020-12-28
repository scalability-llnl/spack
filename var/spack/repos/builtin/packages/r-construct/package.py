# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RConstruct(RPackage):
    """conStruct: Models Spatially Continuous and Discrete Population
       GeneticStructure"""

    homepage = "https://cloud.r-project.org/package=conStruct"
    url      = "https://cloud.r-project.org/src/contrib/conStruct_1.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/conStruct"

    version('1.0.3', sha256='b449c133a944ad05a28f84f312ed4ccbc1574c4659aa09c678618d2ae9008310')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-bh@1.66.0:', type=('build', 'run'))
    depends_on('r-caroline', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.3.0:', type=('build', 'run'))
    depends_on('r-rstan@2.18.1:', type=('build', 'run'))
    depends_on('r-rstantools@1.5.0:', type=('build', 'run'))
    depends_on('r-stanheaders@2.18.0:', type=('build', 'run'))
    depends_on('gmake', type='build')
