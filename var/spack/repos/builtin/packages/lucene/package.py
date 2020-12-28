# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lucene(Package):
    """
    Apache Lucene is a high-performance, full featured text search engine
    library written in Java.
    """

    homepage = "https://lucene.apache.org/"
    url      = "http://archive.apache.org/dist/lucene/java/8.3.1/lucene-8.3.1.tgz"
    list_url = "http://archive.apache.org/dist/lucene/java/"
    list_depth = 1

    version('8.3.1', sha256='acd61ad458d16f3c98b9dd4653c6a34dd666a965842e461f7cdf8947fa041e1a')
    version('8.3.0', sha256='67c4f8081f24ff9f4eb4f2b999ac19f7a639b416e5b6f1c1c74e0524a481fc7e')
    version('8.2.0', sha256='505cad34698b217fd6ceee581a8215223a47df5af820c94ca70a6bdbba9d5d7c')
    version('8.1.1', sha256='d62b0acdf2b1ed7a25ccdb593ad8584caeaa20cc9870e22790d3ec7fa6240a8c')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
