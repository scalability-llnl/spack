# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Emacs(AutotoolsPackage, GNUMirrorPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    git      = "git://git.savannah.gnu.org/emacs.git"
    gnu_mirror_path = "emacs/emacs-24.5.tar.gz"

    version('master', branch='master')
    version('27.1', sha256='ffbfa61dc951b92cf31ebe3efc86c5a9d4411a1222b8a4ae6716cfd0e2a584db')
    version('26.3', sha256='09c747e048137c99ed35747b012910b704e0974dde4db6696fde7054ce387591')
    version('26.2', sha256='4f99e52a38a737556932cc57479e85c305a37a8038aaceb5156625caf102b4eb')
    version('26.1', sha256='760382d5e8cdc5d0d079e8f754bce1136fbe1473be24bb885669b0e38fc56aa3')
    version('25.3', sha256='f72c6a1b48b6fbaca2b991eed801964a208a2f8686c70940013db26cd37983c9')
    version('25.2', sha256='505bbd6ea6c197947001d0f80bfccb6b30e1add584d6376f54d4fd6e4de72d2d')
    version('25.1', sha256='763344b90db4d40e9fe90c5d14748a9dbd201ce544e2cf0835ab48a0aa4a1c67')
    version('24.5', sha256='2737a6622fb2d9982e9c47fb6f2fb297bda42674e09db40fc9bcc0db4297c3b6')

    variant('X', default=False, description="Enable an X toolkit")
    variant(
        'toolkit',
        default='gtk',
        values=('gtk', 'athena'),
        description="Select an X toolkit (gtk, athena)"
    )
    variant('tls', default=False, description="Build Emacs with gnutls")

    depends_on('pkgconfig', type='build')

    depends_on('ncurses')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('libxml2')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='+X toolkit=athena')
    depends_on('gtkplus', when='+X toolkit=gtk')
    depends_on('gnutls', when='+tls')
    depends_on('jpeg')
    depends_on('m4', when="@master:")
    depends_on('autoconf', when="@master:")
    depends_on('automake', when="@master:")
    depends_on('libtool', when="@master:")

    conflicts('@:26.3', when='platform=darwin os=catalina')

    @when('platform=darwin')
    def setup_build_environment(self, env):
        # on macOS, emacs' config does search hard enough for ncurses'
        # termlib `-ltinfo` lib, which results in linker errors
        if '+termlib' in self.spec['ncurses']:
            env.append_flags('LDFLAGS', '-ltinfo')

    def configure_args(self):
        spec = self.spec

        toolkit = spec.variants['toolkit'].value
        if '+X' in spec:
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(toolkit)
            ]
        else:
            args = ['--without-x']

        # On OS X/macOS, do not build "nextstep/Emacs.app", because
        # doing so throws an error at build-time
        if sys.platform == 'darwin':
            args.append('--without-ns')

        if '+tls' in spec:
            args.append('--with-gnutls')
        else:
            args.append('--without-gnutls')

        return args

    def _test_check_versions(self):
        """Perform version checks on installed package binaries."""
        checks = ['ctags', 'ebrowse', 'emacs', 'emacsclient', 'etags']

        for exe in checks:
            expected = str(self.spec.version)
            reason = 'test version of {0} is {1}'.format(exe, expected)
            self.run_test(exe, ['--version'], expected, installed=True,
                          purpose=reason, skip_missing=True)

    def test(self):
        """Perform smoke tests on the installed package."""
        # Simple version check tests on known binaries
        self._test_check_versions()
