# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidycensus(RPackage):
    """An integrated R interface to the decennial US Census and American
    Community Survey APIs and the US Census Bureau's geographic boundary
    files. Allows R users to return Census and ACS data as tidyverse-ready
    data frames, and optionally returns a list-column with feature
    geometry for many geographies."""

    homepage = "https://cloud.r-project.org/package=tidycensus"
    url      = "https://cloud.r-project.org/src/contrib/tidycensus_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tidycensus"

    version('0.9.2', sha256='2454525301caff9eaaf6ebe14f58706ece1fbace6187ce8bf3fff04c842b9536')
    version('0.3.1', sha256='d03cbee7abbf87bb4ce2e649726bdd143d47b549f30b5a11aaaa6c4aff78e778')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-tigris', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-jsonlite@1.5.0:', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rvest', type=('build', 'run'))
    depends_on('r-tidyr@0.7.0:', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-units', type=('build', 'run'))
