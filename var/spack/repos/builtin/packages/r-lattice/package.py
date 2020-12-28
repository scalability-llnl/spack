# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLattice(RPackage):
    """A powerful and elegant high-level data visualization system inspired by
    Trellis graphics, with an emphasis on multivariate data. Lattice is
    sufficient for typical graphics needs, and is also flexible enough to
    handle most nonstandard requirements. See ?Lattice for an introduction."""

    homepage = "http://lattice.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/lattice_0.20-35.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lattice"

    version('0.20-38', sha256='fdeb5e3e50dbbd9d3c5e2fa3eef865132b3eef30fbe53a10c24c7b7dfe5c0a2d')
    version('0.20-35', sha256='0829ab0f4dec55aac6a73bc3411af68441ddb1b5b078d680a7c2643abeaa965d')
    version('0.20-34', sha256='4a1a1cafa9c6660fb9a433b3a51898b8ec8e83abf143c80f99e3e4cf92812518')

    depends_on('r@3.0.0:', type=('build', 'run'))
