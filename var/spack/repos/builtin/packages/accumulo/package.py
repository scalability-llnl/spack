# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Accumulo(MavenPackage):
    """Apache Accumulo is a sorted, distributed key/value store that
    provides robust, scalable data storage and retrieval."""

    homepage = "https://accumulo.apache.org/"
    url      = "https://github.com/apache/accumulo/archive/rel/2.0.0.tar.gz"

    version('2.0.0', sha256='2564056dc24398aa464763c21bae10ef09356fe3261600d27744071cf965c265')
    version('1.9.3', sha256='d9548d5b9cf9f494f027f0fe59d5d6d45d09064359d7761cade62991ce2a5d0c')
    version('1.9.2', sha256='11ab028143ad6313cd5fc701b36b4c35e46a4a3fa2ce663869860b9f6bf5ee4d')

    depends_on('java@8:', type=('build', 'run'))
    depends_on('maven@3.5.0:', type='build')
