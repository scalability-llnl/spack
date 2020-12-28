# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAromaLight(RPackage):
    """Methods for microarray analysis that take basic data types such as
    matrices and lists of vectors. These methods can be used standalone, be
    utilized in other packages, or be wrapped up in higher-level classes."""

    homepage = "https://www.aroma-project.org/"
    git      = "https://git.bioconductor.org/packages/aroma.light"

    version('3.16.0', commit='fc16179fc4bee8954c5415d7cd13e3112b75b4fd')

    depends_on('r@2.15.2:', type=('build', 'run'))
    depends_on('r-r-methodss3@1.7.1:', type=('build', 'run'))
    depends_on('r-r-oo@1.22.0:', type=('build', 'run'))
    depends_on('r-r-utils@2.9.0:', type=('build', 'run'))
    depends_on('r-matrixstats@0.54.0:', type=('build', 'run'))
