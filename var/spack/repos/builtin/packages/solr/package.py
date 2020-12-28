# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Solr(Package):
    """Solr is highly reliable, scalable and fault tolerant, providing distributed
    indexing, replication and load-balanced querying, automated failover and
    recovery,centralized configuration and more. Solr powers the search and
    navigation features of many of the world's largest internet sites."""

    homepage = "https://lucene.apache.org/"
    url      = "https://archive.apache.org/dist/lucene/solr/7.7.3/solr-7.7.3.tgz"
    list_url = "https://archive.apache.org/dist/lucene/solr"
    list_depth = 1

    version('8.6.0', sha256='4519ccdb531619df770f1065db6adcedc052c7aa94b42806d541966550956aa5')
    version('8.5.2', sha256='c457d6c7243241cad141e1df34c6f669d58a6c60e537f4217d032616dd066dcf')
    version('8.5.1', sha256='47b68073b37bbcc0517a355ef722f20827c3f1416537ebbccf5239dda8064a0b')
    version('8.5.0', sha256='9e54711ad0aa60e9723d2cdeb20cf0d21ee2ab9fa0048ec59dcb5f9d94dc61dd')
    version('8.4.1', sha256='ec39e1e024b2e37405149de41e39e875a39bf11a53f506d07d96b47b8d2a4301')
    version('7.7.3', sha256='3ec67fa430afa5b5eb43bb1cd4a659e56ee9f8541e0116d6080c0d783870baee')

    def install(self, spec, prefix):
        install_tree('.', prefix)
