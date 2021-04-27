# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGgplotify(RPackage):
    """Convert Plot to 'grob' or 'ggplot' Object

    Convert plot function call (using expression or formula) to 'grob' or
    'ggplot' object that compatible to the 'grid' and 'ggplot2' ecosystem. With
    this package, we are able to e.g. using 'cowplot' to align plots produced
    by 'base' graphics, 'ComplexHeatmap', 'eulerr', 'grid', 'lattice',
    'magick', 'pheatmap', 'vcd' etc. by converting them to 'ggplot' objects."""

    homepage = "https://github.com/GuangchuangYu/ggplotify"
    url      = "https://cloud.r-project.org/src/contrib/ggplotify_0.0.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggplotify"

    version('0.0.5', sha256='035ea6a70023c4819c8a486d0fd94c2765aa4d6df318747e104eeb9829b9d65d')
    version('0.0.3', sha256='7e7953a2933aa7127a0bac54375e3e0219a0744cfc3249c3d7b76065f7a51892')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gridgraphics', type=('build', 'run'))
    depends_on('r-rvcheck', type=('build', 'run'))
