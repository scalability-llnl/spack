# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSiggenes(RPackage):
    """Multiple Testing using SAM and Efron's Empirical Bayes Approaches.

       Identification of differentially expressed genes and estimation of the
       False Discovery Rate (FDR) using both the Significance Analysis of
       Microarrays (SAM) and the Empirical Bayes Analyses of Microarrays
       (EBAM)."""

    homepage = "https://bioconductor.org/packages/siggenes"
    git      = "https://git.bioconductor.org/packages/siggenes.git"

    version('1.58.0', commit='69500158d69942cf7c62f583830933cf8baf89a1')
    version('1.56.0', commit='3e929feaa76311be07ff51ad807e657b0b521f6f')
    version('1.54.0', commit='1630e42652192e3e4e48e9e78e53665a120cfc7f')
    version('1.52.0', commit='dc46cf4b6053ea99c6c841d661f97390653c2e71')
    version('1.50.0', commit='b1818f26e1449005ffd971df6bda8da0303080bc')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))

    depends_on('r-scrime@1.2.5:', when='@1.58.0:', type=('build', 'run'))
