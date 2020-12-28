# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpparmadillo(RPackage):
    """'Rcpp' Integration for the 'Armadillo' Templated Linear
    Algebra Library."""

    homepage = "https://cloud.r-project.org/package=RcppArmadillo"
    url      = "https://cloud.r-project.org/src/contrib/RcppArmadillo_0.8.100.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppArmadillo"

    version('0.9.600.4.0', sha256='2057b7aa965a4c821dd734276d8e6a01cd59a1b52536b65cb815fa7e8c114f1e')
    version('0.9.400.3.0', sha256='56936d501fe8e6f8796ae1a6badb9294d7dad98a0b557c3b3ce6bd4ecaad13b0')
    version('0.8.100.1.0', sha256='97ca929b34d84d99d7cadc3612b544632cdd0c43ed962933a3d47caa27854fa7')

    depends_on('r@3.3.0:', when='@0.8.500.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
