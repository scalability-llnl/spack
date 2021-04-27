# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRobust(RPackage):
    """Port of the S+ Robust Library

    Methods for robust statistics, a state of the art in the early 2000s,
    notably for robust regression and robust multivariate analysis."""

    homepage = "https://cloud.r-project.org/package=robust"
    url      = "https://cloud.r-project.org/src/contrib/robust_0.4-18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/robust/"

    version('0.5-0.0', sha256='82f0b50028938966f807a4c4da5c345a3a64ccafd9a31c64a22cda852ed345cf')
    version('0.4-18.1', sha256='de31901882873ef89748bb6863caf55734431df5b3eb3c6663ed17ee2e4a4077')
    version('0.4-18', sha256='e4196f01bb3b0d768759d4411d524238b627eb8dc213d84cb30014e75480f8ac')

    depends_on('r-fit-models', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-rrcov', type=('build', 'run'))
