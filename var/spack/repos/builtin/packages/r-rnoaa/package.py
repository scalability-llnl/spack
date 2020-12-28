# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRnoaa(RPackage):
    """rnoaa: 'NOAA' Weather Data from R"""

    homepage = "https://github.com/ropensci/rnoaa"
    url      = "https://cloud.r-project.org/src/contrib/rnoaa_0.8.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rnoaa"

    version('0.8.4', sha256='fb9ae771111dd5f638c1eff3290abad2ff9cc7e68a6678bf2414433ebed2dbbf')

    depends_on('r-crul@0.7.0:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-geonames', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-hoardr@0.5.2:', type=('build', 'run'))
    depends_on('r-isdparser@0.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lubridate', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
