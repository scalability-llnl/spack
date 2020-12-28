# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgrepel(RPackage):
    """ggrepel: Repulsive Text and Label Geoms for 'ggplot2'"""

    homepage = "http://github.com/slowkow/ggrepel"
    url      = "https://cloud.r-project.org/src/contrib/ggrepel_0.6.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggrepel"

    version('0.8.1', sha256='d5d03a77ab6d8c831934bc46e840cc4e3df487272ab591fa72767ad42bcb7283')
    version('0.8.0', sha256='6386606e716d326354a29fcb6cd09f9b3d3b5e7c5ba0d5f7ff35416b1a4177d4')
    version('0.6.5', sha256='360ae9d199755f9e260fefbd3baba3448fad3f024f20bcd9942a862b8c41a752')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-scales@0.3.0:', type=('build', 'run'))
