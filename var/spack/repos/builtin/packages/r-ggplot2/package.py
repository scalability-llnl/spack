# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGgplot2(RPackage):
    """Create Elegant Data Visualisations Using the Grammar of Graphics

    A system for 'declaratively' creating graphics, based on "The Grammar of
    Graphics". You provide the data, tell 'ggplot2' how to map variables to
    aesthetics, what graphical primitives to use, and it takes care of the
    details."""

    homepage = "http://ggplot2.org/"
    url      = "https://cloud.r-project.org/src/contrib/ggplot2_2.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggplot2"

    version('3.3.3', sha256='45c29e2348dbd195bbde1197a52db7764113e57f463fd3770fb899acc33423cc')
    version('3.2.0', sha256='31b6897fb65acb37913ff6e2bdc1b57f652360098ae3aa660abdcf54f84d73b3')
    version('3.1.1', sha256='bfde297f3b4732e7f560078f4ce131812a70877e6b5b1d41a772c394939e0c79')
    version('2.2.1', sha256='5fbc89fec3160ad14ba90bd545b151c7a2e7baad021c0ab4b950ecd6043a8314')
    version('2.1.0', sha256='f2c323ae855d6c089e3a52138aa7bc25b9fe1429b8df9eae89d28ce3c0dd3969')

    depends_on('r@3.1:', when='@:3.1.1', type=('build', 'run'))
    depends_on('r@3.2:', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-glue', when='@3.3.3:', type=('build', 'run'))
    depends_on('r-gtable@0.1.1:', type=('build', 'run'))
    depends_on('r-isoband', when='@3.3.3:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mgcv', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-scales@0.5.0:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-withr@2.0.0:', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-plyr@1.7.1:', when='@:3.1.1', type=('build', 'run'))
    depends_on('r-reshape2', when='@:3.2.0', type=('build', 'run'))
    depends_on('r-lazyeval', when='@:3.2.0', type=('build', 'run'))
    depends_on('r-viridislite', when='@3.0.0:3.2.0', type=('build', 'run'))
