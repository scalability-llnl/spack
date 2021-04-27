# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBiocversion(RPackage):
    """Set the appropriate version of Bioconductor packages

    This package provides repository information for the appropriate
    version of Bioconductor."""

    homepage = "https://bioconductor.org/packages/BiocVersion/"
    git      = "https://git.bioconductor.org/packages/BiocVersion"

    version('3.12.0', commit='23b971963c6b73550a7e330dab5a046d58ce0223')

    depends_on('r@4.0.0:', type=('build', 'run'))
