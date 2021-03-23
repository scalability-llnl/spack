# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class W3m(AutotoolsPackage):
    """
    w3m is a text-based web browser as well as a pager like `more' or `less'.
    With w3m you can browse web pages through a terminal emulator window (xterm,
    rxvt or something like that). Moreover, w3m can be used as a text formatting
    tool which typesets HTML into plain text.
    """

    homepage = "http://w3m.sourceforge.net/index.en.html"
    url      = "https://downloads.sourceforge.net/project/w3m/w3m/w3m-0.5.3/w3m-0.5.3.tar.gz"

    maintainers = ['ronin_gw']

    version('0.5.3', sha256='e994d263f2fd2c22febfbe45103526e00145a7674a0fda79c822b97c2770a9e3')

    # mandatory dependency
    depends_on('bdw-gc')

    # termlib
    variant('termlib', default='ncurses', description='select termlib',
            values=('ncurses', 'termcap', 'none'), multi=False)
    depends_on('termcap', when='termlib=termcap')
    depends_on('ncurses+termlib', when='termlib=ncurses')

    # https support
    variant('https', default=True, description='support https protocol')
    depends_on('openssl@:1.0.2u', when='+https')

    # X11 support
    variant('image', default=True, description='enable image')
    depends_on('libx11', when='+image')

    # inline image support
    variant('imagelib', default='imlib2', description='select imagelib',
            values=('gdk-pixbuf', 'imlib2'), multi=False)
    depends_on('gdk-pixbuf@2:+x11', when='imagelib=gdk-pixbuf +image')
    depends_on('imlib2@1.0.5:', when='imagelib=imlib2 +image')

    # fix for modern libraries
    patch('fix_redef.patch')
    patch('fix_gc.patch')

    def _add_arg_for_variant(self, args, variant, choices):
        for avail_lib in choices:
            if self.spec.variants[variant].value == avail_lib:
                args.append('--with-{0}={1}'.format(variant, avail_lib))
                return

    def configure_args(self):
        args = []

        self._add_arg_for_variant(args, 'termlib', ('termcap', 'ncurses'))
        if '+image' in self.spec:
            args.append('--enable-image')
            self._add_arg_for_variant(args, 'imagelib', ('gdk-pixbuf', 'imlib2'))

        return args

    def setup_build_environment(self, env):
        if self.spec.variants['termlib'].value == 'ncurses':
            env.append_flags('LDFLAGS', '-ltinfo')
            env.append_flags('LDFLAGS', '-lncurses')
        if '+image' in self.spec:
            env.append_flags('LDFLAGS', '-lX11')

    # parallel build causes build failure
    def build(self, spec, prefix):
        make(parallel=False)
