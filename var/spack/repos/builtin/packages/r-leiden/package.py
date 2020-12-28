# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeiden(RPackage):
    """Implements the 'Python leidenalg' module to be called in R. Enables
    clustering using the leiden algorithm for partition a graph into
    communities. See the 'Python' repository for more details:
        <https://github.com/vtraag/leidenalg> Traag et al (2018) From Louvain
        to Leiden: guaranteeing well-connected communities.
        <arXiv:1810.08473>."""

    homepage = "https://github.com/TomKellyGenetics/leiden"
    url      = "https://cloud.r-project.org/src/contrib/leiden_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/leiden"

    version('0.3.1', sha256='17fa1e49667fdd30ef5166506181c8514ae406f68f0878a026ee111bff11f8a5')

    depends_on('r-reticulate', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
