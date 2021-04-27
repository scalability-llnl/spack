# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RQuickplot(RPackage):
    """A System of Plotting Optimized for Speed and Modularity

    A high-level plotting system, built using 'grid' graphics, that
    is optimized for speed and modularity. This has great utility
    for quick visualizations when testing code, with the key benefit
    that visualizations are updated independently of one another."""

    homepage = "http://quickplot.predictiveecology.org/"
    url      = "https://cloud.r-project.org/src/contrib/quickPlot_0.1.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/quickPlot"

    maintainers = ['dorton21']

    version('0.1.6', sha256='48690a77ae961ed1032130621ef06b2eaf86ee592bf1057471a8c6d6a98ace55')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-backports', type=('build', 'run'))
    depends_on('r-data-table@1.10.4:', type=('build', 'run'))
    depends_on('r-fpcompare', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gridbase', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-rgdal', type=('build', 'run'))
    depends_on('r-rgeos', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
