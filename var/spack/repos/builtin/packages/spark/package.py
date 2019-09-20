# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class Spark(Package):
    """Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "http://spark.apache.org"

    variant('hadoop', default=False,
            description='Build with Hadoop')

    depends_on('java@8', type=('build', 'run'))
    depends_on('hadoop', when='+hadoop', type=('build', 'run'))

    version('2.4.0', 'b1d6d6cb49d8253b36df8372a722292bb323bd16315d83f0b0bafb66a4154ef2')
    version('2.3.0', 'db21021b8e877b219ab886097ef42344')
    version('2.1.0', '21d4471e78250775b1fa7c0e6c3a1326')
    version('2.0.2', '32110c1bb8f081359738742bd26bced1')
    version('2.0.0', '8a5307d973da6949a385aefb6ff747bb')
    version('1.6.2', '304394fbe2899211217f0cd9e9b2b5d9')
    version('1.6.1', 'fcf4961649f15af1fea78c882e65b001')
    version('1.6.0', '2c28edc89ca0067e63e525c04f7b1d89')

    def url_for_version(self, version):
        url = "http://archive.apache.org/dist/spark/spark-{0}/spark-{0}-bin-{1}.tgz"
        if self.spec.satisfies('@2.4.0: +hadoop'):
            checksums = {
                Version('2.4.0'): 'c93c096c8d64062345b26b34c85127a6848cff95a4bb829333a06b83222a5cfa'
            }
            self.versions[version] = {'checksum': checksums[version]}
            return url.format(version, 'hadoop2.7')
        return url.format(version, 'without-hadoop')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('conf')
        install_dir('jars')
        install_dir('python')
        install_dir('R')
        install_dir('sbin')
        install_dir('yarn')

        # required for spark to recognize binary distribution
        install('RELEASE', prefix)

    @when('+hadoop')
    def setup_environment(self, spack_env, run_env):
        hadoop = self.spec['hadoop'].command
        hadoop.add_default_env('JAVA_HOME', self.spec['java'].home)
        hadoop_classpath = hadoop('classpath', output=str)

        # Remove whitespaces, as they can compromise syntax in
        # module files
        hadoop_classpath = re.sub(r'[\s+]', '', hadoop_classpath)

        run_env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)
