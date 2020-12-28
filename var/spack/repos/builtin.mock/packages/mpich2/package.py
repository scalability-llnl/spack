# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpich2(Package):
    homepage   = "http://www.mpich.org"
    url        = "http://www.mpich.org/static/downloads/1.5/mpich2-1.5.tar.gz"
    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    tags = ['tag1', 'tag3']

    version('1.5', '9c5d5d4fe1e17dd12153f40bc5b6dbc0')
    version('1.4', 'foobarbaz')
    version('1.3', 'foobarbaz')
    version('1.2', 'foobarbaz')
    version('1.1', 'foobarbaz')
    version('1.0', 'foobarbaz')

    provides('mpi@:2.0')
    provides('mpi@:2.1', when='@1.1:')
    provides('mpi@:2.2', when='@1.2:')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
