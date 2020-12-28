# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGrbase(RPackage):
    """gRbase: A Package for Graphical Modelling in R"""

    homepage = "http://people.math.aau.dk/~sorenh/software/gR/"
    url      = "https://cloud.r-project.org/src/contrib/gRbase_1.8-3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gRbase"

    version('1.8-3.4', sha256='d35f94c2fb7cbd4ce3991570424dfe6723a849658da32e13df29f53b6ea2cc2c')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
