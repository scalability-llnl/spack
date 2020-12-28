# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShiny(RPackage):
    """Makes it incredibly easy to build interactive web applications with R.
    Automatic "reactive" binding between inputs and outputs and extensive
    pre-built widgets make it possible to build beautiful, responsive, and
    powerful applications with minimal effort."""

    homepage = "http://shiny.rstudio.com/"
    url      = "https://cloud.r-project.org/src/contrib/shiny_1.0.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shiny"

    version('1.3.2', sha256='28b851ae6c196ca845f6e815c1379247595ac123a4faa10a16533d1a9ce0c24f')
    version('1.0.5', sha256='20e25f3f72f3608a2151663f7836f2e0c6da32683a555d7541063ae7a935fa42')
    version('0.13.2', sha256='0fe7e952f468242d7c43ae49afcc764788f7f2fd5436d18c3d20a80db7296231')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-httpuv@1.5.0:', type=('build', 'run'))
    depends_on('r-mime@0.3:', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.16:', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-r6@2.0:', type=('build', 'run'))
    depends_on('r-sourcetools', type=('build', 'run'))
    depends_on('r-later@0.7.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-promises@1.0.1:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-crayon', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@1.1.0:', type=('build', 'run'))
