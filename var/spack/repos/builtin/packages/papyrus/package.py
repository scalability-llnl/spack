# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Papyrus(CMakePackage):
    """Parallel Aggregate Persistent Storage"""

    homepage = "https://code.ornl.gov/eck/papyrus"
    url      = "https://code.ornl.gov/eck/papyrus/repository/archive.tar.bz2?ref=v1.0.2"
    git      = "https://code.ornl.gov/eck/papyrus.git"

    version('master', branch='master')
    version('1.0.2', sha256='b6cfcff99f73ded8e4ca4b165bc182cd5cac60f0c0cf4f93649b77d074445645')
    version('1.0.1', sha256='3772fd6f2c301faf78f18c5e4dc3dbac57eb361861b091579609b3fff9e0bb17')
    version('1.0.0', sha256='5d57c0bcc80de48951e42460785783b882087a5714195599d773a6eabde5c4c4')

    depends_on('mpi')

    test_requires_compiler = True

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.prepend_path('CPATH', self.prefix.include)
        env.prepend_path('LIBRARY_PATH', lib_dir)
        env.prepend_path('LD_LIBRARY_PATH', lib_dir)

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([join_path('kv', 'tests', '01_open_close')])

    def run_01_open_close_test(self):
        """Run stand alone test: 01_open_close"""

        test_dir = join_path(self.test_suite.current_test_cache_dir,
                            'kv', 'tests', '01_open_close')

        if not os.path.exists(test_dir):
            print('Skipping 01_open_close test')
            return

        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        exe = 'test01_open_close'

        options = ['-I{0}'.format(join_path(self.prefix, 'include')),
                   '-L{0}'.format(lib_dir), '-lpapyruskv', '-g', '-o',
                   exe, 'test01_open_close.c', '-lpthread', '-lm']

        self.run_test(self.spec['mpi'].mpicxx, options,
                      purpose  ='test: compile {0} example'.format(exe),
                      work_dir =test_dir)

        self.run_test(exe,
                      purpose='test: run {0} example'.format(exe),
                      work_dir=test_dir)

    def test(self):
        self.run_01_open_close_test()
