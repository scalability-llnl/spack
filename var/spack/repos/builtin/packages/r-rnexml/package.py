# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRnexml(RPackage):
    """RNeXML: Semantically Rich I/O for the 'NeXML' Format.

    Provides access to phyloinformatic data in 'NeXML' format. The package
    should add new functionality to R such as the possibility to manipulate
    'NeXML' objects in more various and refined way and compatibility with
    'ape' objects."""

    homepage = "https://github.com/ropensci/RNeXML"
    url      = "https://cloud.r-project.org/src/contrib/RNeXML_2.4.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RNeXML"

    version('2.4.5', sha256='2b667ecb6400e4c0c125ca73a98cde81330cde3a85b764261f77159e702754f3')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-ape@3.1:', type=('build', 'run'))
    depends_on('r-xml@3.95:', type=('build', 'run'))
    depends_on('r-plyr@1.8:', type=('build', 'run'))
    depends_on('r-reshape2@1.2.2:', type=('build', 'run'))
    depends_on('r-httr@0.3:', type=('build', 'run'))
    depends_on('r-uuid@0.1-1:', type=('build', 'run'))
    depends_on('r-dplyr@0.5.0:', type=('build', 'run'))
    depends_on('r-lazyeval@0.1.0:', type=('build', 'run'))
    depends_on('r-tidyr@0.3.1:', type=('build', 'run'))
    depends_on('r-stringr@1.0:', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
