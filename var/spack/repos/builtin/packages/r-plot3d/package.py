# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPlot3d(RPackage):
    """Plotting Multi-Dimensional Data

    Functions for viewing 2-D and 3-D data, including perspective plots, slice
    plots, surface plots, scatter plots, etc. Includes data sets from
    oceanography."""

    homepage = "https://cloud.r-project.org/package=plot3D"
    url      = "https://cloud.r-project.org/src/contrib/plot3D_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plot3D"

    version('1.3', sha256='b9e4ec2789e34ad249318900e186868650e1a33466b385cb492a45466db3dfc9')
    version('1.1.1', sha256='f6fe4a001387132626fc553ed1d5720d448b8064eb5a6917458a798e1d381632')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@2.15:', type=('build', 'run'))
    depends_on('r-misc3d', type=('build', 'run'))
