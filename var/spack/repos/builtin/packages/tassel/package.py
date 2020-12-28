# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tassel(Package):
    """TASSEL is a software package to evaluate traits associations,
       evolutionary patterns, and linkage disequilibrium."""

    homepage = "http://www.maizegenetics.net/tassel"
    git      = "https://bitbucket.org/tasseladmin/tassel-5-standalone.git"

    version('2017-07-22', commit='ae96ae75c3c9a9e8026140b6c775fa4685bdf531')

    depends_on('java', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path('CLASSPATH', self.prefix.bin.lib)
