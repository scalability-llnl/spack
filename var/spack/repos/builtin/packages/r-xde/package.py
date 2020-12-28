# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXde(RPackage):
    """XDE: a Bayesian hierarchical model for cross-study analysis of
       differential gene expression."""

    homepage = "https://bioconductor.org/packages/XDE"
    git      = "https://git.bioconductor.org/packages/XDE.git"

    version('2.30.0', commit='058af6f1e431522778f970bf61f834620d3d7dd7')
    version('2.28.0', commit='b8cc7d0840ce1324644e8b4a750fbb964884498b')
    version('2.26.0', commit='7bf6368037937c53542447175061c2e2059ee3be')
    version('2.24.0', commit='fd5f245f82893657dc36e5a67a1d3b8255772462')
    version('2.22.0', commit='25bcec965ae42a410dd285a9db9be46d112d8e81')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-biobase@2.5.5:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-mergemaid', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))

    depends_on('r-rcolorbrewer', when='@2.24.0:', type=('build', 'run'))
    depends_on('r-genemeta', when='@2.24.0:', type=('build', 'run'))
    depends_on('r-siggenes', when='@2.24.0:', type=('build', 'run'))
