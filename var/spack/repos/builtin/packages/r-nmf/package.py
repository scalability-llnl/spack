# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNmf(RPackage):
    """Provides a framework to perform Non-negative Matrix Factorization (NMF).
    The package implements a set of already published algorithms and seeding
    methods, and provides a framework to test, develop and plug new/custom
    algorithms. Most of the built-in algorithms have been optimized in C++, and
    the main interface function provides an easy way of performing parallel
    computations on multicore machines.."""

    homepage = "http://renozao.github.io/NMF"
    url      = "https://cloud.r-project.org/src/contrib/NMF_0.21.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/NMF"

    version('0.21.0', sha256='3b30c81c66066fab4a63c5611a0313418b840d8b63414db31ef0e932872d02e3')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-pkgmaker@0.20:', type=('build', 'run'))
    depends_on('r-registry', type=('build', 'run'))
    depends_on('r-rngtools@1.2.3:', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-stringr@1.0.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gridbase', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
