# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidygraph(RPackage):
    """tidygraph: A Tidy API for Graph Manipulation.

    A graph, while not "tidy" in itself, can be thought of as two tidy data
    frames describing node and edge data respectively. 'tidygraph' provides an
    approach to manipulate these two virtual data frames using the API defined
    in the 'dplyr' package, as well as provides tidy interfaces to a lot of
    common graph algorithms."""

    homepage = "https://github.com/thomasp85/tidygraph"
    url      = "https://cloud.r-project.org/src/contrib/tidygraph_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tidygraph"

    version('1.1.2', sha256='5642001d4cccb122d66481b7c61a06c724c02007cbd356ee61cb29726a56fafe')

    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-dplyr@0.8:', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-pillar', type=('build', 'run'))
