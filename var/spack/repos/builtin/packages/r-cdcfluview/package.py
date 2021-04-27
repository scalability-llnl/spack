# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCdcfluview(RPackage):
    """Retrieve Flu Season Data from the United States Centers for Disease
    Control and Prevention ('CDC') 'FluView' Portal

    The 'U.S.' Centers for Disease Control ('CDC') maintains a portal
    <http://gis.cdc.gov/grasp/fluview/fluportaldashboard.html> for accessing
    state, regional and national influenza statistics as well as Mortality
    Surveillance Data. The web interface makes it difficult and time-consuming
    to select and retrieve influenza data. Tools are provided to access the
    data provided by the portal's underlying 'API'."""

    homepage = "https://cloud.r-project.org/package=cdcfluview"
    url      = "https://cloud.r-project.org/src/contrib/cdcfluview_0.7.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cdcfluview"

    version('0.9.2', sha256='f2080fc80c5e0241f8b657f5ac3a251ea89dfc26c1ab13bdfaed4d4e97495015')
    version('0.9.0', sha256='1b2064886858cbb1790ef808d88fbab75d3a9cf55e720638221a3377ff8dd244')
    version('0.7.0', sha256='8c8978d081f8472a6ed5ec54c4e6dd906f97ee28d0f88eef1514088f041ecc03')

    depends_on('r@3.2.0:', when='@:0.9.0', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@0.9.2:', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-progress', when='@0.9.2:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-tibble', when='@0.9.2:', type=('build', 'run'))
    depends_on('r-sf', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-mmwrweek', type=('build', 'run'))
    depends_on('r-units@0.4-6:', type=('build', 'run'))
