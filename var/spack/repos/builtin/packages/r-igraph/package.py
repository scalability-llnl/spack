# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIgraph(RPackage):
    """Routines for simple graphs and network analysis. It can handle large
    graphs very well and provides functions for generating random and regular
    graphs, graph visualization, centrality methods and much more."""

    homepage = "http://igraph.org/"
    url      = "https://cloud.r-project.org/src/contrib/igraph_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/igraph"

    version('1.2.4.1', sha256='891acc763b5a4a4a245358a95dee69280f4013c342f14dd6a438e7bb2bf2e480')
    version('1.2.4', sha256='1048eb26ab6b592815bc269c1d91e974c86c9ab827ccb80ae0a40042019592cb')
    version('1.1.2', sha256='89b16b41bc77949ea208419e52a18b78b5d418c7fedc52cd47d06a51a6e746ec')
    version('1.0.1', sha256='dc64ed09b8b5f8d66ed4936cde3491974d6bc5178dd259b6eab7ef3936aa5602')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pkgconfig@2.0.0:', type=('build', 'run'))
    depends_on('r-irlba', when='@:1.1.9', type=('build', 'run'))
    depends_on('gmp')
    depends_on('libxml2')
    depends_on('glpk', when='@1.2.0:')
