# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hiredis(MakefilePackage):
    """Hiredis is a minimalistic C client library for the Redis database."""

    homepage = "https://github.com/redis/hiredis"
    url      = "https://github.com/redis/hiredis/archive/v0.14.1.tar.gz"

    version('0.14.1', sha256='2663b2aed9fd430507e30fc5e63274ee40cdd1a296026e22eafd7d99b01c8913')
    version('0.14.0', sha256='042f965e182b80693015839a9d0278ae73fae5d5d09d8bf6d0e6a39a8c4393bd')
    version('0.13.3', sha256='717e6fc8dc2819bef522deaca516de9e51b9dfa68fe393b7db5c3b6079196f78')
    version('0.13.2', sha256='b0cf73ebe039fe25ecaaa881acdda8bdc393ed997e049b04fc20865835953694')

    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
