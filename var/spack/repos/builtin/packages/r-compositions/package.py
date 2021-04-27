# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCompositions(RPackage):
    """Compositional Data Analysis

    Provides functions for the consistent analysis of compositional  data (e.g.
    portions of substances) and positive numbers (e.g. concentrations)  in the
    way proposed by J. Aitchison and V. Pawlowsky-Glahn."""

    homepage = "https://cloud.r-project.org/package=compositions"
    url      = "https://cloud.r-project.org/src/contrib/compositions_1.40-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/compositions"

    version('2.0-1', sha256='84a291308faf858e5a9d9570135c2da5e57b0887f407903485fa85d09da61a0f')
    version('1.40-2', sha256='110d71ae000561987cb73fc76cd953bd69d37562cb401ed3c36dca137d01b78a')

    depends_on('r@2.2.0:', type=('build', 'run'))
    depends_on('r-tensora', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-bayesm', type=('build', 'run'))
    depends_on('r-mass', when='@2.0-1:', type=('build', 'run'))
    depends_on('r-energy', when='@:1.40-2', type=('build', 'run'))
