# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdegraphics(RPackage):
    """adegraphics: An S4 Lattice-Based Package for the Representation of
    Multivariate Data.

    Graphical functionalities for the representation of multivariate data.
    It is a complete re-implementation of the functions available in the 'ade4'
    package."""

    homepage = "http://pbil.univ-lyon1.fr/ADE-4"
    url      = "https://cloud.r-project.org/src/contrib/adegraphics_1.0-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/adegraphics"

    version('1.0-15', sha256='87bbcd072e9a898955f5ede4315e82365086a50a2887bf5bd2e94bbb4d3f678a')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-ade4@1.7-13:', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-latticeextra', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-sp@1.1-1:', type=('build', 'run'))
