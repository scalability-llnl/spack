# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fpocket(MakefilePackage):
    """fpocket is a very fast open source protein pocket detection algorithm
       based on Voronoi tessellation."""

    homepage = "https://github.com/Discngine/fpocket"
    version('master', branch='master',
            git='https://github.com/Discngine/fpocket.git')

    depends_on("netcdf-c")

    def setup_build_environment(self, env):
        if self.compiler.name == 'gcc':
            env.set('CXX', 'g++')

    def edit(self):
        makefile = FileFilter('makefile')
        makefile.filter('BINDIR .*', 'BINDIR = %s/bin' % self.prefix)
        makefile.filter('MANDIR .*', 'MANDIR = %s/man/man8' % self.prefix)
