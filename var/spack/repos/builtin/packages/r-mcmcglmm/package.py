# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMcmcglmm(RPackage):
    """MCMC Generalised Linear Mixed Models."""

    homepage = "https://cloud.r-project.org/package=MCMCglmm"
    url      = "https://cloud.r-project.org/src/contrib/MCMCglmm_2.25.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MCMCglmm"

    version('2.29', sha256='13ba7837ea2049e892c04e7ec5c83d5b599a7e4820b9d875f55ec40fc2cc67b4')
    version('2.28', sha256='7d92e6d35638e5e060a590b92c3b1bfc02a11386276a8ab99bceec5d797bfc2a')
    version('2.25', sha256='3072316bf5c66f6db5447cb488395ff019f6c47122813467384474f340643133')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-corpcor', type=('build', 'run'))
    depends_on('r-tensora', type=('build', 'run'))
    depends_on('r-cubature', type=('build', 'run'))
