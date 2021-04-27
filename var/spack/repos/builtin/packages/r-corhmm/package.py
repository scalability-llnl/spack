# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCorhmm(RPackage):
    """Hidden Markov Models of Character Evolution

    Fits hidden Markov models of discrete character evolution which allow
    different transition rate classes on different portions of a phylogeny.
    Beaulieu et al (2013) <doi:10.1093/sysbio/syt034>."""

    homepage = "https://cloud.r-project.org/package=corHMM"
    url      = "https://cloud.r-project.org/src/contrib/corHMM_1.22.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/corHMM/"

    version('2.6', sha256='726de9707ede8ef447915171a3abe1003a0e42fe8e17eb440442cac9adf8cdcf')
    version('1.22', sha256='d262fa1183eab32087afb70f1789fabae6fb49bec01d627974c54a088a48b10d')

    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-nloptr', type=('build', 'run'))
    depends_on('r-gensa', type=('build', 'run'))
    depends_on('r-expm', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
    depends_on('r-corpcor', type=('build', 'run'))
    depends_on('r-mass', when='@2.6:', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-phangorn', type=('build', 'run'))
    depends_on('r-viridis', when='@2.6:', type=('build', 'run'))
    depends_on('r-rmpfr', type=('build', 'run'))
    depends_on('r-igraph', when='@2.6:', type=('build', 'run'))
    depends_on('r-phytools', when='@2.6:', type=('build', 'run'))
