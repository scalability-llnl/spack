# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCorhmm(RPackage):
    """corHMM: Analysis of Binary Character Evolution

       Fits a hidden rates model that allows different transition rate classes
       on different portions of a phylogeny by treating rate classes as hidden
       states in a Markov process and various other functions for evaluating
       models of binary character evolution."""

    homepage = "https://cloud.r-project.org/package=corHMM"
    url      = "https://cloud.r-project.org/src/contrib/corHMM_1.22.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/corHMM/"

    version('1.22', sha256='d262fa1183eab32087afb70f1789fabae6fb49bec01d627974c54a088a48b10d')

    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-nloptr', type=('build', 'run'))
    depends_on('r-gensa', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-corpcor', type=('build', 'run'))
    depends_on('r-phangorn', type=('build', 'run'))
    depends_on('r-rmpfr', type=('build', 'run'))
