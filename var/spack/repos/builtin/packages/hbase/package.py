# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hbase(Package):
    """Apache HBase is an open-source, distributed, versioned, column-oriented
    store modeled after Google' Bigtable: A Distributed Storage System for
    Structured Data by Chang et al. Just as Bigtable leverages the distributed
    data storage provided by the Google File System, HBase provides
    Bigtable-like capabilities on top of Apache Hadoop."""

    homepage = "https://archive.apache.org/"
    url      = "https://archive.apache.org/dist/hbase/2.2.4/hbase-2.2.4-bin.tar.gz"
    list_url = "https://archive.apache.org/dist/hbase"
    list_depth = 1

    version('2.2.5',  sha256='25d08f8f038d9de5beb43dfb0392e8a8b34eae7e0f2670d6c2c172abc3855194')
    version('2.2.4',  sha256='ec91b628352931e22a091a206be93061b6bf5364044a28fb9e82f0023aca3ca4')
    version('2.2.3',  sha256='ea8fa72aa6220e038e30bd7c439d181b10bd7225383f7f2d224ebb5f5397310a')
    version('2.2.2',  sha256='97dcca3a031925a379a0ee6bbfb6007533fb4fdb982c23345e5fc04d6c52bebc')
    version('2.1.8',  sha256='d8296e8405b1c39c73f0dd03fc6b4d2af754035724168fd56e8f2a0ff175ad90')

    depends_on('java@8', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
