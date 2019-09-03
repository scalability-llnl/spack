# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGraph(RPackage):
    """graph: A package to handle graph data structures.

       A package that implements some simple graph handling capabilities."""

    homepage = "https://bioconductor.org/packages/graph"
    git      = "https://git.bioconductor.org/packages/graph.git"

    version('1.62.0', commit='95223bd63ceb66cfe8d881f992a441de8b8c89a3')
    version('1.60.0', commit='e2aecb0a862f32091b16e0036f53367d3edf4c1d')
    version('1.58.2', commit='6455d8e7a5a45dc733915942cb71005c1016b6a0')
    version('1.56.0', commit='c4abe227dac525757679743e6fb4f49baa34acad')
    version('1.54.0', commit='2a8b08520096241620421078fc1098f4569c7301')

    depends_on('r@3.6.0:3.6.9', when='@1.62.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.60.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.58.2', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.56.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.54.0', type=('build', 'run'))

    depends_on('r-biocgenerics@0.13.11:', when='@1.54.0:', type=('build', 'run'))
