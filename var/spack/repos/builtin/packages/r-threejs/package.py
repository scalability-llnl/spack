# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RThreejs(RPackage):
    """Create interactive 3D scatter plots, network plots, and globes using the
    'three.js' visualization library ("http://threejs.org")."""

    homepage = "http://bwlewis.github.io/rthreejs"
    url      = "https://cloud.r-project.org/src/contrib/threejs_0.2.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/threejs"

    version('0.3.1', sha256='71750b741672a435ecf749b69c72f0681aa8bb795e317f4e3056d5e33f6d79e8')
    version('0.2.2', sha256='41fe949490fbe0f71e39b0a144791da427bd7361d027579cb4a002ed53520cc5')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-htmlwidgets@0.3.2:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-matrix', when='@0.2.2', type=('build', 'run'))
    depends_on('r-jsonlite', when='@0.2.2', type=('build', 'run'))
    depends_on('r-igraph@1.0.0:', when='@0.3.1:', type=('build', 'run'))
    depends_on('r-crosstalk', when='@0.3.1:', type=('build', 'run'))
