# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPheatmap(RPackage):
    """Pretty Heatmaps

    Implementation of heatmaps that offers more control over dimensions and
    appearance."""

    homepage = "https://cloud.r-project.org/package=pheatmap"
    url      = "https://cloud.r-project.org/src/contrib/pheatmap_1.0.12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pheatmap"

    version('1.0.12', sha256='579d96ee0417203b85417780eca921969cda3acc210c859bf9dfeff11539b0c1')

    depends_on('r@2.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
