# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lz4Java(Package):
    """LZ4 compression for Java"""

    homepage = "https://github.com/lz4/lz4-java"
    url      = "https://github.com/lz4/lz4-java/archive/1.7.1.tar.gz"

    version('1.7.1', sha256='2e5c4546788eddc76dd91008faa60f96059b216997a7e6009c97b0b2ba2b4ff7')

    depends_on('ant', type='build')
    depends_on('lz4', type='build')
    depends_on('xxhash', type='build')
    depends_on('java', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.prepend_path('CPATH', self.spec['xxhash'].prefix.include)
        env.prepend_path('CPATH', self.spec['lz4'].prefix.include)

    @run_before('install')
    def create_lz4_lib_dir(self):
        mkdirp('src/lz4/lib')

    def install(self, spec, prefix):
        ant = which('ant')
        ant('ivy-bootstrap')
        ant()
        install_tree('.', prefix)
