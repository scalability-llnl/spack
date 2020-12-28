# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Conflict(Package):
    homepage = 'https://github.com/tgamblin/callpath'
    url = 'http://github.com/tgamblin/callpath-1.0.tar.gz'

    version(0.8, 'foobarbaz')
    version(0.9, 'foobarbaz')
    version(1.0, 'foobarbaz')

    variant('foo', default=True, description='')

    conflicts('%clang', when='+foo')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")

    def setup_environment(self, senv, renv):
        renv.set('FOOBAR', self.name)
