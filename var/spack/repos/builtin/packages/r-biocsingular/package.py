# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocsingular(RPackage):
    """Singular Value Decomposition for Bioconductor Packages.

       Implements exact and approximate methods for singular value
       decomposition and principal components analysis, in a framework that
       allows them to be easily switched within Bioconductor packages or
       workflows. Where possible, parallelization is achieved using the
       BiocParallel framework."""

    homepage = "https://bioconductor.org/packages/BiocSingular"
    git      = "https://git.bioconductor.org/packages/BiocSingular.git"

    version('1.0.0', commit='d2b091c072d0312698c9bb6611eb1bdf8aebf833')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-delayedarray', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('r-rsvd', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-beachmat', type=('build', 'run'))
