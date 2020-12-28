# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDeldir(RPackage):
    """Calculates the Delaunay triangulation and the Dirichlet or Voronoi
    tessellation (with respect to the entire plane) of a planar point set.
    Plots triangulations and tessellations in various ways. Clips
    tessellations to sub-windows. Calculates perimeters of tessellations.
    Summarises information about the tiles of the tessellation."""

    homepage = "https://cloud.r-project.org/package=deldir"
    url      = "https://cloud.r-project.org/src/contrib/deldir_0.1-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/deldir"

    version('0.1-23', sha256='e0112bce9fc94daf73596a0fff9b3958b80872e3bbb487be73e157b13a6f201d')
    version('0.1-21', sha256='b9dabcc1813c7a0f8edaf720a94bdd611a83baf3d3e52e861d352369e815690c')
    version('0.1-14', sha256='89d365a980ef8589971e5d311c6bd59fe32c48dbac8000a880b9655032c99289')

    depends_on('r@0.99:', type=('build', 'run'))
