# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RErgm(RPackage):
    """An integrated set of tools to analyze and simulate networks based
       on exponential-family random graph models (ERGM). "ergm" is a
       part of the "statnet" suite of packages for network analysis."""

    homepage = "http://statnet.org"
    url      = "https://cloud.r-project.org/src/contrib/ergm_3.7.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ergm"

    version('3.10.4', sha256='885f0b1a23c5a2c1947962350cfab66683dfdfd1db173c115e90396d00831f22')
    version('3.10.1', sha256='a2ac249ff07ba55b3359242f20389a892543b4fff5956d74143d2d41fa6d4beb')
    version('3.7.1', sha256='91dd011953b93ecb2b84bb3ababe7bddae25d9d86e69337156effd1da84b54c3')

    depends_on('r-robustbase@0.93-5:', type=('build', 'run'))
    depends_on('r-coda@0.19-2:', type=('build', 'run'))
    depends_on('r-trust@0.1.7:', type=('build', 'run'))
    depends_on('r-matrix@1.2-17:', type=('build', 'run'))
    depends_on('r-lpsolve@5.6.13:', type=('build', 'run'))
    depends_on('r-mass@7.3-51.4:', type=('build', 'run'))
    depends_on('r-statnet-common@4.3.0:', type=('build', 'run'))
    depends_on('r-network@1.15:', type=('build', 'run'))
    depends_on('r-purrr@0.3.2:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.4:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-tibble@2.1.1:', when='@3.10.0:', type=('build', 'run'))
    depends_on('r-dplyr@0.8.0.1:', when='@3.10.0:', type=('build', 'run'))
    # The CRAN page list OpenMPI as a dependency but this is not a dependency
    # for using the package. If one wishes to use MPI, simply load an MPI
    # package, along with r-dosnow and r-rmpi when using r-ergm, and set the
    # appropriate options in the R script.
