# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeomorph(RPackage):
    """Read, manipulate, and digitize landmark data, generate shape variables
       via Procrustes analysis for points, curves and surfaces, perform shape
       analyses, and provide graphical depictions of shapes and patterns of
       shape variation."""

    homepage = "https://cloud.r-project.org/package=geomorph"
    url      = "https://cloud.r-project.org/src/contrib/geomorph_3.0.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/geomorph"

    version('3.1.2', sha256='29cf1c484f756cb44808cfdbc20137a6fbc4bd0c5c6f98c6c3f397c5aebda8f1')
    version('3.1.1', sha256='8eb222011433100860b308beef6f02ade7c421785f575ab4461ee25e38dfa1bd')
    version('3.0.7', sha256='68f8942e1a5bc3f0298c9f5b8f69c4702c8e12ecb2275d740fda4d04d66d38e1')
    version('3.0.5', sha256='7a3a587b253770a5e7e70536234dee13e6a073f1fdf1d644ae4f11d2eb95b104')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-geiger', when='@:3.1.1', type=('build', 'run'))
    depends_on('r-matrix', when='@:3.1.1', type=('build', 'run'))
    depends_on('r-rrpp', type=('build', 'run'), when='@3.0.7:')
