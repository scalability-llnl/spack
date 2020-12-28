# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocparallel(RPackage):
    """Bioconductor facilities for parallel evaluation.

       This package provides modified versions and novel implementation of
       functions for parallel evaluation, tailored to use with Bioconductor
       objects."""

    homepage = "https://bioconductor.org/packages/BiocParallel"
    git      = "https://git.bioconductor.org/packages/BiocParallel.git"

    version('1.18.1', commit='348264af782d7dcd41a1879400f348f836767f6e')
    version('1.16.6', commit='7f7a54c47f4949b600b9fd568289a519496bc4d4')
    version('1.14.2', commit='1d5a44960b19e9dbbca04c7290c8c58b0a7fc299')
    version('1.12.0', commit='2143a9addceed0151a27b95c70aadd2add5cbace')
    version('1.10.1', commit='a76c58cf99fd585ba5ea33065649e68f1afe0a7d')

    depends_on('r-futile-logger', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))

    depends_on('r-bh', when='@1.12.0:', type=('build', 'run'))
