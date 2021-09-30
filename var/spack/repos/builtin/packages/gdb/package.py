# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Gdb(AutotoolsPackage, GNUMirrorPackage):
    """GDB, the GNU Project debugger, allows you to see what is going on
    'inside' another program while it executes -- or what another
    program was doing at the moment it crashed.
    """

    homepage = "https://www.gnu.org/software/gdb"
    gnu_mirror_path = "gdb/gdb-7.10.tar.gz"

    maintainers = ['robertu94']

    version('11.1', sha256='cc2903474e965a43d09c3b263952d48ced39dd22ce2d01968f3aa181335fcb9c')
    version('10.2',   sha256='b33ad58d687487a821ec8d878daab0f716be60d0936f2e3ac5cf08419ce70350')
    version('10.1',   sha256='f12f388b99e1408c01308c3f753313fafa45517740c81ab7ed0d511b13e2cf55')
    version('9.2',    sha256='38ef247d41ba7cc3f6f93a612a78bab9484de9accecbe3b0150a3c0391a3faf0')
    version('9.1',    sha256='fcda54d4f35bc53fb24b50009a71ca98410d71ff2620942e3c829a7f5d614252')
    version('8.3.1',  sha256='26ce655216cd03f4611518a7a1c31d80ec8e884c16715e9ba8b436822e51434b')
    version('8.3',    sha256='b2266ec592440d0eec18ee1790f8558b3b8a2845b76cc83a872e39b501ce8a28')
    version('8.2.1',  sha256='0107985f1edb8dddef6cdd68a4f4e419f5fec0f488cc204f0b7d482c0c6c9282')
    version('8.2',    sha256='847e4b65e5a7b872e86019dd59659029e2b06cae962e0ef345f169dcb4b851b8')
    version('8.1',    sha256='e54a2322da050e4b00785370a282b9b8f0b25861ec7cfbbce0115e253eea910e')
    version('8.0.1',  sha256='52017d33cab5b6a92455a1a904046d075357abf24153470178c0aadca2d479c5')
    version('8.0',    sha256='8968a19e14e176ee026f0ca777657c43456514ad41bb2bc7273e8c4219555ac9')
    version('7.12.1', sha256='142057eacecfb929d52b561eb47a1103c7d504cec3f659dd8a5ae7bc378f7e77')
    version('7.11',   sha256='9382f5534aa0754169e1e09b5f1a3b77d1fa8c59c1e57617e06af37cb29c669a')
    version('7.10.1', sha256='ff14f8050e6484508c73cbfa63731e57901478490ca1672dc0b5e2b03f6af622')
    version('7.10',   sha256='50690e6d6b7917a6544190ec9401eaafb555e3cef8981709ea9870296c383ce5')
    version('7.9.1',  sha256='4994ad986726ac4128a6f1bd8020cd672e9a92aa76b80736563ef992992764ef')
    version('7.9',    sha256='d282508cb7df0cb8b2cf659032ce1bede7b5725796e3ac90f3cd9d65844a65f2')
    version('7.8.2',  sha256='fd9a9784ca24528aac8a4e6b8d7ae7e8cf0784e128cd67a185c986deaf6b9929')

    variant('python', default=True, description='Compile with Python support')
    variant('xz', default=True, description='Compile with lzma support')
    variant('source-highlight', default=False, description='Compile with source-highlight support')
    variant('lto', default=False, description='Enable lto')
    variant('quad', default=False, description='Enable quad')
    variant('gold', default=False, description='Enable gold linker')
    variant('ld', default=False, description='Enable ld')
    variant('tui', default=False, description='Enable tui')

    # Resolves the undefined references to libintl_gettext while linking gdbserver
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
    patch('gdb-libintl-10.patch', level=0, when='@10.1:11.0')
    patch('gdb-libintl-11.patch', level=0, when='@11.1:')

    # Silence warnings about imp being deprecated on new python versions
    # https://sourceware.org/pipermail/gdb-patches/2021-February/176622.html
    patch('importlib.patch', when="@8.3.1:10.2 ^python@3.4:")

    # Required dependency
    depends_on('texinfo', type='build')

    # Optional dependencies
    depends_on('python+debug', when='+python', type=('build', 'link', 'run'))
    depends_on('xz', when='+xz')
    depends_on('source-highlight', when='+source-highlight')
    depends_on('ncurses', when='+tui')
    depends_on('gmp', when='@11.1:')

    build_directory = 'spack-build'

    def configure_args(self):
        args = [
            '--with-system-gdbinit={0}'.format(self.prefix.etc.gdbinit)
        ]

        if self.spec.version >= Version("11.1"):
            args.append("--with-gmp={}".format(self.spec['gmp'].prefix))

        if '+python' in self.spec:
            args.append('--with-python={}'.format(self.spec['python'].command))
            args.append('LDFLAGS={0}'.format(
                self.spec['python'].libs.ld_flags))

        if '+lto' in self.spec:
            args.append('--enable-lto')

        if '+quad' in self.spec:
            args.append('--with-quad')

        if '+gold' in self.spec:
            args.append('--enable-gold')

        if '+ld' in self.spec:
            args.append('--enable-ld')

        if '+tui' in self.spec:
            args.append('--enable-tui')

        return args

    @run_after('install')
    def gdbinit(self):
        if '+python' in self.spec:
            tool = self.spec['python'].command.path + '-gdb.py'
            if os.path.exists(tool):
                mkdir(self.prefix.etc)
                with open(self.prefix.etc.gdbinit, 'w') as gdbinit:
                    gdbinit.write('add-auto-load-safe-path {0}\n'.format(tool))
