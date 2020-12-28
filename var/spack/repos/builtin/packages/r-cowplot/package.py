# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCowplot(RPackage):
    """Some helpful extensions and modifications to the 'ggplot2'
    package. In particular, this package makes it easy to combine
    multiple 'ggplot2' plots into one and label them with letters,
    e.g. A, B, C, etc., as is often required for scientific
    publications. The package also provides a streamlined and clean
    theme that is used in the Wilke lab, hence the package name,
    which stands for Claus O. Wilke's plot package."""

    homepage = "https://cloud.r-project.org/package=cowplot"
    url      = "https://cloud.r-project.org/src/contrib/cowplot_0.8.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cowplot"

    version('1.0.0', sha256='70f9a7c46d10f409d1599f1afc9fd3c947051cf2b430f01d903c64ef1e6c98a5')
    version('0.9.3', sha256='3e10475fd7506ea9297ed72eb1a3acf858c6fa99d26e46fc39654eba000c3dcb')
    version('0.9.2', sha256='8b92ce7f92937fde06b0cfb86c7634a39b3b2101e362cc55c4bec6b3fde1d28f')
    version('0.9.1', sha256='953fd9d6ff370472b9f5a9ee867a423bea3e26e406d08a2192ec1872a2e60047')
    version('0.9.0', sha256='d5632f78294c3678c08d3eb090abe1eec5cc9cd15cb5d96f9c43794ead098cb5')
    version('0.8.0', sha256='a617fde25030fe764f20967fb753a953d73b47745a2146c97c2565eb4d06700d')

    depends_on('r@3.3.0:', when='@:0.9.4', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.0.0:', type=('build', 'run'))
    depends_on('r-ggplot2@2.1.1:', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-plyr@1.8.2:', when='@:0.9.9', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-rlang', when='@1.0.0:', type=('build', 'run'))
