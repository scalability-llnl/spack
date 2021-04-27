# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class REnergy(RPackage):
    """Statistics: Multivariate Inference via the Energy of Data

    E-statistics (energy) tests and statistics for multivariate and univariate
    inference, including distance correlation, one-sample, two-sample, and
    multi-sample tests for comparing multivariate distributions, are
    implemented. Measuring and testing multivariate independence based on
    distance correlation, partial distance correlation, multivariate
    goodness-of-fit tests, k-groups and hierarchical clustering based on energy
    distance, testing for multivariate normality, distance components (disco)
    for non-parametric  analysis of structured data, and other energy
    statistics/methods are implemented."""

    homepage = "https://cloud.r-project.org/package=energy"
    url      = "https://cloud.r-project.org/src/contrib/energy_1.7-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/energy"

    version('1.7-7', sha256='67b88fb33ee6e7bec2e4fe356a4efd36f70c3cf9b0ebe2f6d9da9ec96de9968f')
    version('1.7-6', sha256='900edbb28e1f1bccd78580828470628cf75eb6333b63e1a58e4da7fc5c5fa89a')
    version('1.7-5', sha256='24c2cf080939f8f56cd9cda06d2dfc30d0389cd3ec7250af4f9a09a4c06b6996')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.6:', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
