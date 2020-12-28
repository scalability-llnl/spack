# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RDiversitree(RPackage):
    """Contains a number of comparative 'phylogenetic' methods.

       Mostly focusing on analysing diversification and character
       evolution. Contains implementations of 'BiSSE' (Binary State
       'Speciation' and Extinction) and its unresolved tree extensions,
       'MuSSE' (Multiple State 'Speciation' and Extinction), 'QuaSSE',
       'GeoSSE', and 'BiSSE-ness' Other included methods include Markov
       models of discrete and continuous trait evolution and constant
       rate 'speciation' and extinction."""

    homepage = "http://www.zoology.ubc.ca/prog/diversitree"
    url      = "https://cloud.r-project.org/src/contrib/diversitree_0.9-10.tar.gz"
    list_url = "https://cron.r-project.org/src/contrib/Archive/diversitree"

    version('0.9-11', sha256='4caa6a468f93de9f1c8c30e4457f34bb8346e1acdaf74f684005bfa86a950ecb')
    version('0.9-10', sha256='e7df5910c8508a5c2c2d6d3deea53dd3f947bb762196901094c32a7033cb043e')

    depends_on('r@2.1.0:', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-desolve@1.7:', type=('build', 'run'))
    depends_on('r-subplex', type=('build', 'run'))
    depends_on('r-rcpp@0.10.0:', type=('build', 'run'))
    depends_on('fftw@3.1.2:')
    depends_on('gsl@1.15:')
