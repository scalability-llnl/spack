# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGrbase(RPackage):
    """A Package for Graphical Modelling in R

    The 'gRbase' package provides graphical modelling features used by e.g. the
    packages 'gRain', 'gRim' and 'gRc'. 'gRbase' implements graph algorithms
    including (i) maximum cardinality search (for marked and unmarked graphs).
    (ii) moralization, (iii) triangulation, (iv) creation of junction tree.
    'gRbase' facilitates array operations, 'gRbase' implements functions for
    testing for conditional independence. 'gRbase' illustrates how hierarchical
    log-linear models may be implemented and describes concept of graphical
    meta data.  The facilities of the package are documented in the book by
    Hojsgaard, Edwards and Lauritzen (2012, <doi:10.1007/978-1-4614-2299-0>)
    and in the paper by  Dethlefsen and Hojsgaard, (2005,
    <doi:10.18637/jss.v014.i17>).  Please see 'citation("gRbase")' for citation
    details.  NOTICE  'gRbase' requires that the packages graph, 'Rgraphviz'
    and 'RBGL' are installed from 'bioconductor'; for installation instructions
    please refer to the web page given below."""

    homepage = "http://people.math.aau.dk/~sorenh/software/gR/"
    url      = "https://cloud.r-project.org/src/contrib/gRbase_1.8-3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gRbase"

    version('1.8-6.7', sha256='aaafc7e1b521de60e1a57c0175ac64d4283850c3273bd14774cf24dabc743388')
    version('1.8-3.4', sha256='d35f94c2fb7cbd4ce3991570424dfe6723a849658da32e13df29f53b6ea2cc2c')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.6.0:', when='@1.8-6.7:', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rgraphviz', when='@1.8-6.7:', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
