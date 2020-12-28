# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ConflictParent(Package):
    homepage = 'https://github.com/tgamblin/callpath'
    url = 'http://github.com/tgamblin/callpath-1.0.tar.gz'

    version(0.8, 'foobarbaz')
    version(0.9, 'foobarbaz')
    version(1.0, 'foobarbaz')

    depends_on('conflict')

    conflicts('^conflict~foo', when='@0.9')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")

    def setup_environment(self, senv, renv):
        renv.set('FOOBAR', self.name)
