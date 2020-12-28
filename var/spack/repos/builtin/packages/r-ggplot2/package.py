# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgplot2(RPackage):
    """An implementation of the grammar of graphics in R. It combines the
    advantages of both base and lattice graphics: conditioning and shared axes
    are handled automatically, and you can still build up a plot step by step
    from multiple data sources. It also implements a sophisticated
    multidimensional conditioning system and a consistent interface to map data
    to aesthetic attributes. See http://ggplot2.org for more information,
    documentation and examples."""

    homepage = "http://ggplot2.org/"
    url      = "https://cloud.r-project.org/src/contrib/ggplot2_2.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggplot2"

    version('3.2.0', sha256='31b6897fb65acb37913ff6e2bdc1b57f652360098ae3aa660abdcf54f84d73b3')
    version('3.1.1', sha256='bfde297f3b4732e7f560078f4ce131812a70877e6b5b1d41a772c394939e0c79')
    version('2.2.1', sha256='5fbc89fec3160ad14ba90bd545b151c7a2e7baad021c0ab4b950ecd6043a8314')
    version('2.1.0', sha256='f2c323ae855d6c089e3a52138aa7bc25b9fe1429b8df9eae89d28ce3c0dd3969')

    depends_on('r@3.1:', when='@:3.1.1', type=('build', 'run'))
    depends_on('r@3.2:', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-gtable@0.1.1:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-plyr@1.7.1:', when='@:3.1.1', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-scales@0.5.0:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-mgcv', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-rlang@0.3.0:', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-viridislite', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-withr@2.0.0:', when='@3.0.0:', type=('build', 'run'))
