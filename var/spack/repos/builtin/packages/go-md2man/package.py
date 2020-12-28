# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GoMd2man(Package):
    """go-md2man converts markdown into roff (man pages)"""

    homepage = "https://github.com/cpuguy83/go-md2man"
    url      = "https://github.com/cpuguy83/go-md2man/archive/v1.0.10.tar.gz"

    version('1.0.10', sha256='76aa56849123b99b95fcea2b15502fd886dead9a5c35be7f78bdc2bad6be8d99')

    depends_on('go')

    resource(name='blackfriday',
             url='https://github.com/russross/blackfriday/archive/v1.5.2.tar.gz',
             sha256='626138a08abb8579474a555e9d45cb5260629a2c07e8834428620a650dc9f195',
             placement='blackfriday',
             destination=join_path('src', 'github.com', 'russross'))

    def patch(self):
        mkdirp(join_path(self.stage.source_path,
               'src', 'github.com', 'russross'))

        mkdirp(join_path(self.stage.source_path,
               'src', 'github.com', 'cpuguy83'))

        ln = which('ln')
        ln('-s', self.stage.source_path, join_path(
           'src', 'github.com', 'cpuguy83', 'go-md2man'))

    def install(self, spec, prefix):

        with working_dir('src'):
            env['GOPATH'] = self.stage.source_path
            env['GO111MODULE'] = 'off'
            go = which('go')
            go('build', '-v', join_path(
               'github.com', 'cpuguy83', 'go-md2man'))

            mkdir(prefix.bin)
            install('go-md2man', prefix.bin)
