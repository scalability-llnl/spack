# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RShadowtext(RPackage):
    """Shadow Text Grob and Layer

    Implement shadowtextGrob() for 'grid' and geom_shadowtext() layer for
    'ggplot2'. These functions create/draw text grob with background shadow."""

    homepage = "https://github.com/GuangchuangYu/shadowtext/"
    url      = "https://cloud.r-project.org/src/contrib/shadowtext_0.0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/shadowtext"

    version('0.0.7', sha256='6e32b1dfd3d4816803848b876666185258b888286ec3d3e8500499ec3eba31e8')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
