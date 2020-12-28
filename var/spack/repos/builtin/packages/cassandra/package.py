# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cassandra(Package):
    """
    Apache Cassandra is a highly-scalable partitioned row store. Rows are
    organized into tables with a required primary key.
    """

    homepage = "https://github.com/apache/cassandra"
    url      = "https://github.com/apache/cassandra/archive/cassandra-4.0-alpha2.tar.gz"

    version('4.0-alpha2', sha256='6a8e99d8bc51efd500981c85c6aa547387b2fdbedecd692308f4632dbc1de3ba')
    version('4.0-alpha1', sha256='2fdf5e3d6c03a29d24a09cd52bb17575e5faccdc4c75a07edd63a9bf4f740105')
    version('3.11.6',     sha256='a739ad036d58f95b5526c481b20773cfcc9ccf3c9dc0b50943d9f2306b56e824', preferred=True)
    version('3.11.5',     sha256='0ee3da12a2be86d7e03203fcc56c3589ddb38347b9cd031495a2b7fcf639fea6')

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('.', prefix)
