# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSpadesTools(RPackage):
    """Tools for Spatially Explicit Discrete Event Simulation (SpaDES) Models

    Provides GIS and map utilities, plus additional modeling tools for developing
    cellular automata, dynamic raster models, and agent based models in 'SpaDES'.
    Included are various methods for spatial spreading, spatial agents, GIS
    operations, random map generation, and others. See '?SpaDES.tools' for an
    categorized overview of these additional tools."""

    homepage = "https://spades-tools.predictiveecology.org/"
    url      = "https://cloud.r-project.org/src/contrib/SpaDES.tools_0.3.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/SpaDES.tools"

    maintainers = ['dorton21']

    version('0.3.6', sha256='661f8ee792874e7447be78103775b63f18ec69e773a7b275dd977adb406dd3e5')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-backports', type=('build', 'run'))
    depends_on('r-checkmate@1.8.2:', type=('build', 'run'))
    depends_on('r-circstats@0.2-4:', type=('build', 'run'))
    depends_on('r-data-table@1.10.4:', type=('build', 'run'))
    depends_on('r-fastmatch@1.1-0:', type=('build', 'run'))
    depends_on('r-fpcompare@0.2.1:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-quickplot', type=('build', 'run'))
    depends_on('r-raster@2.5-8:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
    depends_on('r-reproducible@0.2.0:', type=('build', 'run'))
    depends_on('r-rgeos', type=('build', 'run'))
    depends_on('r-sp@1.2-4:', type=('build', 'run'))
