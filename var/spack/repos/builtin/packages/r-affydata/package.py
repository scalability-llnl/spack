# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffydata(RPackage):
    """Affymetrix Data for Demonstration Purpose.

       Example datasets of a slightly large size. They represent 'real world
       examples', unlike the artificial examples included in the package
       affy."""

    homepage = "https://bioconductor.org/packages/affydata"
    git      = "https://git.bioconductor.org/packages/affydata.git"

    version('1.32.0', commit='c7cef93f6edd23024f4b1985b90e89058874c2bd')
    version('1.30.0', commit='d5408d84b37ebae73b40a448dd52baf7b4a13bea')
    version('1.28.0', commit='a106a5514c352bf0bbc624ded58a93886d4ce96f')
    version('1.26.0', commit='eb0a44a39990b361f9fb1094837ffafb320f39a9')
    version('1.24.0', commit='663991606507572f083232e2b393d901270291d4')

    depends_on('r@2.4.0:', type=('build', 'run'))
    depends_on('r-affy@1.23.4:', type=('build', 'run'))
