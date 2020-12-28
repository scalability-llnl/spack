# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAde4(RPackage):
    """Analysis of Ecological Data : Exploratory and Euclidean Methods in
    Environmental Sciences"""

    homepage = "http://pbil.univ-lyon1.fr/ADE-4"
    url      = "https://cloud.r-project.org/src/contrib/ade4_1.7-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ade4"

    version('1.7-13', sha256='f5d0a7356ae63f82d3adb481a39007e7b0d70211b8724aa686af0c89c994e99b')
    version('1.7-11', sha256='4ccd799ae99bd625840b866a697c4a48adb751660470bf0d6cf9207b1927a572')
    version('1.7-6', sha256='80848e1650dcc0ec921c130efa6f7e9b307f0d107c63e49faa52296eda19cc52')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
