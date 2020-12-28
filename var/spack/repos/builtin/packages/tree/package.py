# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Tree(Package):
    """Tree is a recursive directory listing command that produces a depth
       indented listing of files, which is colorized ala dircolors if
       the LS_COLORS environment variable is set and output is to
       tty. Tree has been ported and reported to work under the
       following operating systems: Linux, FreeBSD, OS X, Solaris,
       HP/UX, Cygwin, HP Nonstop and OS/2."""

    homepage = "http://mama.indstate.edu/users/ice/tree/"
    url      = "http://mama.indstate.edu/users/ice/tree/src/tree-1.7.0.tgz"

    version('1.8.0', sha256='715d5d4b434321ce74706d0dd067505bb60c5ea83b5f0b3655dae40aa6f9b7c2')
    version('1.7.0', sha256='6957c20e82561ac4231638996e74f4cfa4e6faabc5a2f511f0b4e3940e8f7b12')

    def install(self, spec, prefix):
        objs = [
            'tree.o',
            'unix.o',
            'html.o',
            'xml.o',
            'json.o',
            'hash.o',
            'color.o'
        ]
        # version 1.8.0 added file.c
        if spec.version >= Version('1.8.0'):
            objs.append('file.o')

        if (sys.platform == 'darwin'):
            objs.append('strverscmp.o')

        args = [
            'prefix=%s' % prefix,
            'CC=%s' % spack_cc,
            'CFLAGS=',
            'OBJS=%s' % ' '.join(objs),
            'install'
        ]

        make(*args)
