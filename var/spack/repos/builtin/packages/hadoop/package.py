# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hadoop(MavenPackage):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models."""

    homepage = "http://hadoop.apache.org/"
    url      = "https://github.com/apache/hadoop/archive/rel/release-3.2.1.tar.gz"

    version('3.2.1', sha256='43ccc9078afb51c7d22087613b52cf7ad3ed8737371d6353c16af3b93069fb8b')
    version('3.1.3', sha256='1ebe5bf73589b4a5284b8bf04b93cb14808f8350653988d8c50ecf7b2a931837')
    version('3.1.1', sha256='00f6eb11144525d426fe4dabcc9ddb5f6080cceb96b2cb77d2a55f0713412c20')
    version('3.1.0', sha256='42c540101ee8c50e4c90ba7a430a75459afb1802211e7d4a09ee694eb0157631')

    depends_on('protobuf@2.5.0')
    depends_on('java@8', type=('build', 'run'))
    depends_on('cmake', type='build')
    depends_on('openssl')
    depends_on('libtirpc')
    depends_on('doxygen', type='build', when='@3.2.1:')
    depends_on('cyrus-sasl', when='@3.2.1:')

    def setup_build_environment(self, env):
        env.append_path('LDFLAGS', '-ldl -ltirpc')
        env.prepend_path('CPATH', self.spec['libtirpc'].prefix.include.tirpc)

    def build(self, spec, prefix):
        mvn = which('mvn')
        mvn('package', '-DskipTests', '-Pdist,native',
            '-Dtar', '-Dmaven.javadoc.skip=true')

    def install(self, spec, prefix):
        hadoop_path = join_path(self.stage.source_path,
                                'hadoop-dist', 'target',
                                'hadoop-{0}'.format(self.version))
        with working_dir(hadoop_path):
            install_tree('.', prefix)
