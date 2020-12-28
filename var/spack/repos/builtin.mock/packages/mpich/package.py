# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpich(Package):
    homepage   = "http://www.mpich.org"
    url        = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    tags = ['tag1', 'tag2']

    variant('debug', default=False,
            description="Compile MPICH with debug flags.")

    version('3.0.4', '9c5d5d4fe1e17dd12153f40bc5b6dbc0')
    version('3.0.3', 'foobarbaz')
    version('3.0.2', 'foobarbaz')
    version('3.0.1', 'foobarbaz')
    version('3.0', 'foobarbaz')
    version('1.0', 'foobarbas')

    provides('mpi@:3', when='@3:')
    provides('mpi@:1', when='@:1')

    def install(self, spec, prefix):
        touch(prefix.mpich)
