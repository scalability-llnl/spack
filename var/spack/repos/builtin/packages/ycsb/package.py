# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ycsb(MavenPackage):
    """Yahoo! Cloud Serving Benchmark."""

    homepage = "https://research.yahoo.com/news/yahoo-cloud-serving-benchmark/"
    url      = "https://github.com/brianfrankcooper/YCSB/archive/0.17.0.tar.gz"
    git      = "https://github.com/brianfrankcooper/YCSB.git"

    version('0.17.0', sha256='5dd1a3d4dd7ac336eadccc83b097c811e142cfe1b23fc278f247054a1892c0e0')
    version('0.16.0', sha256='4296fd5e90d7d6d7dfcbad90039ddf16e785706a07f99c1c8a06e6ee06440f71')
    version('0.15.0', sha256='50b83c11f1a2f19f45e3cc6781f952c69944d1221dfec72169c3587802fc7fbb')
    version('0.14.0', sha256='456bcc9fa3d5d66d76fffa9cec34afd4528d9f02aa8a8d1135f511650516d5cb')
    version('0.13.0', sha256='21cb8078a0fe2d8d909145744ca15848dbb6757e98a7fdc97fb4049f82f4afbc')

    depends_on('maven@3.1.0:', type='build')
    depends_on('mongodb-async-driver', type='build')

    def build(self, spec, prefix):
        mvn = which('mvn')
        jar_name = 'target/mongodb-async-driver-' + \
            spec['mongodb-async-driver'].version.string + '.jar'
        path = join_path(self.spec['mongodb-async-driver'].prefix, jar_name)
        mvn('install:install-file', '-Dfile={0}'.format(path),
            '-DgroupId=com.allanbank', '-DartifactId=mongodb-async-driver',
            '-Dversion=2.0.1', '-Dpackaging=jar')
        mvn('package', '-DskipTests')
