# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pathfinder(MakefilePackage):
    """Proxy Application. Signature search."""

    homepage = "https://mantevo.org/packages/"
    url      = "http://mantevo.org/downloads/releaseTarballs/miniapps/PathFinder/PathFinder_1.0.0.tgz"

    tags = ['proxy-app']

    version('1.0.0', '374269e8d42c305eda3e392444e22dde')

    build_targets = ['--directory=PathFinder_ref', 'CC=cc']

    def edit(self, spec, prefix):
        makefile = FileFilter('PathFinder_ref/Makefile')
        makefile.filter('-fopenmp', self.compiler.openmp_flag)

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install('PathFinder_ref/PathFinder.x', prefix.bin)
        install('PathFinder_ref/MicroTestData.adj_list', prefix.bin)
        install('README', prefix.doc)

        install_tree('generatedData/', prefix.doc.generatedData)
        install_tree('scaleData/', prefix.doc.scaleData)
