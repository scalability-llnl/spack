# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exa(Package):
    """exa is a replacement for ls written in Rust."""

    homepage = 'https://the.exa.website'
    url = 'https://github.com/ogham/exa/archive/v0.9.0.tar.gz'

    version('0.9.0', sha256='96e743ffac0512a278de9ca3277183536ee8b691a46ff200ec27e28108fef783')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')
