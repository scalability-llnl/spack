# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPhilentropy(RPackage):
    """Computes 46 optimized distance and similarity measures for comparing
    probability functions (Drost (2018) <doi:10.21105/joss.00765>). These
    comparisons between probability functions have their foundations in a broad
    range of scientific disciplines from mathematics to ecology. The aim of
    this package is to provide a core framework for clustering, classification,
    statistical inference, goodness-of-fit, non-parametric statistics,
    information theory, and machine learning tasks that are based on comparing
    univariate or multivariate probability functions."""

    homepage = "https://github.com/HajkD/philentropy"
    url      = "https://cloud.r-project.org/src/contrib/philentropy_0.4.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/philentropy"

    version('0.4.0', sha256='bfd30bf5635aab6a82716299a87d44cf96c7ab7f4ee069843869bcc85c357127')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
