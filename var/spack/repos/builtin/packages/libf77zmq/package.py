# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Libf77zmq(MakefilePackage):
    """Fortran binding for the ZeroMQ communication library"""

    homepage = "http://zguide.zeromq.org/"
    url      = "https://github.com/zeromq/f77_zmq/archive/4.3.1.tar.gz"

    maintainers = ['scemama']

    version('4.3.1', sha256='a15d72d93022d3e095528d2808c7767cece974a2dc0e2dd95e4c122f60fcf0a8')

    depends_on('libzmq')
    depends_on('python', type='build')

    def setup_build_environment(self, env):
        env.append_flags('CFLAGS', '-O3')
        env.append_flags('CFLAGS', '-g')

    def edit(self, spec, prefix):
        cflags = os.environ.get('CFLAGS')
        makefile = FileFilter('Makefile')
        makefile.filter('CC=.*',
                        'CC={0} {1}'.format(self.compiler.cc,
                                            self.compiler.pic_flag))
        makefile.filter('CFLAGS=.*', 'CFLAGS={0}'.format(cflags))
        makefile.filter('PREFIX=.*', 'PREFIX={0}'.format(self.prefix))
        ZMQ_H = "{0}/include/zmq.h".format(self.spec['libzmq'].prefix)
        os.environ['ZMQ_H'] = ZMQ_H
        os.mkdir("{0}/include".format(self.prefix))
        os.mkdir("{0}/lib".format(self.prefix))

    def install(self, spec, prefix):
        make()
        make('install')
