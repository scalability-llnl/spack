# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


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

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        env.prepend_path('CPATH', self.prefix.include)
        env.prepend_path('LIBRARY_PATH', lib_dir)
        env.prepend_path('LD_LIBRARY_PATH', lib_dir)
