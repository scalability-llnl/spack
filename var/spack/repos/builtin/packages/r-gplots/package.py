# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
#
from spack import *


class RGplots(RPackage):
    """Various R Programming Tools for Plotting Data.

    Various R programming tools for plotting data, including:
    [1] calculating and plotting locally smoothed summary function as
    ('bandplot', 'wapply'),
    [2] enhanced versions of standard plots ('barplot2', 'boxplot2',
    'heatmap.2', 'smartlegend'),
    [3] manipulating colors ('col2hex', 'colorpanel', 'redgreen', 'greenred',
    'bluered', 'redblue', 'rich.colors'),
    [4] calculating and plotting two-dimensional data summaries ('ci2d',
    'hist2d'),
    [5] enhanced regression diagnostic plots ('lmplot2', 'residplot'),
    [6] formula-enabled interface to 'stats::lowess' function ('lowess'),
    [7] displaying textual data in plots ('textplot', 'sinkplot'),
    [8] plotting a matrix where each cell contains a dot whose size reflects
    the relative magnitude of the elements ('balloonplot'),
    [9] plotting "Venn" diagrams ('venn'),
    [10] displaying Open-Office style plots ('ooplot'),
    [11] plotting multiple data on same region, with separate axes
    ('overplot'),
    [12] plotting means and confidence intervals ('plotCI', 'plotmeans'),
    [13] spacing points in an x-y plot so they don't overlap ('space')."""

    cran = "gplots"

    version('3.1.1', sha256='f9ae19c2574b6d41adbeccaf7bc66cf56d7b2769004daba7e0038d5fbd821339')
    version('3.0.1.1', sha256='7db103f903a25d174cddcdfc7b946039b61e236c95084b90ad17f1a41da3770c')
    version('3.0.1', sha256='343df84327ac3d03494992e79ee3afc78ba3bdc08af9a305ee3fb0a38745cb0a')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))

    depends_on('r-gdata', type=('build', 'run'), when='@:3.0.1.1')
