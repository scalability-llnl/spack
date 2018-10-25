# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Luit(Package):
    """Luit is a filter that can be run between an arbitrary application and
    a UTF-8 terminal emulator such as xterm.  It will convert application
    output from the locale's encoding into UTF-8, and convert terminal
    input from UTF-8 into the locale's encoding."""

    homepage = "http://cgit.freedesktop.org/xorg/app/luit"
    url      = "https://www.x.org/archive/individual/app/luit-1.1.1.tar.gz"

    version('1.1.1', '04128a52f68c05129f709196819ddad3')

    depends_on('libfontenc')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix),
                  # see http://www.linuxquestions.org/questions/linux-from-scratch-13/can't-compile-luit-xorg-applications-4175476308/  # noqa
                  'CFLAGS=-U_XOPEN_SOURCE -D_XOPEN_SOURCE=600')

        make()
        make('install')
