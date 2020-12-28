# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Rhash(MakefilePackage):
    """RHash is a console utility for computing and verifying hash sums of
    files. It supports CRC32, MD4, MD5, SHA1, SHA256, SHA512, SHA3, Tiger,
    TTH, Torrent BTIH, AICH, ED2K, GOST R 34.11-94, RIPEMD-160, HAS-160,
    EDON-R 256/512, WHIRLPOOL and SNEFRU hash sums."""

    homepage = "https://sourceforge.net/projects/rhash/"
    url      = "https://github.com/rhash/RHash/archive/v1.3.5.tar.gz"

    version('1.3.5', sha256='98e0688acae29e68c298ffbcdbb0f838864105f9b2bd8857980664435b1f1f2e')

    # For macOS build instructions, see:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/rhash.rb

    def build(self, spec, prefix):
        # Doesn't build shared libraries by default
        make('PREFIX={0}'.format(prefix))

        if spec.satisfies('platform=darwin'):
            make('PREFIX={0}'.format(prefix), '-C', 'librhash', 'dylib')
        else:
            make('PREFIX={0}'.format(prefix), 'lib-shared')

    def check(self):
        # Makefile has both `test` and `check` targets:
        #
        # * `test`  - used to test that the build is working properly
        # * `check` - used to check that the tarball is ready for upload
        #
        # Default implmentation is to run both `make test` and `make check`.
        # `test` passes, but `check` fails, so only run `test`.
        make('test')
        make('test-static-lib')

        if not self.spec.satisfies('platform=darwin'):
            make('test-shared')
            make('test-shared-lib')

    def install(self, spec, prefix):
        # Some things are installed to $(DESTDIR)$(PREFIX) while other things
        # are installed to $DESTDIR/etc.
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
        make('install-lib-static', 'DESTDIR={0}'.format(prefix), 'PREFIX=')

        if spec.satisfies('platform=darwin'):
            install('librhash/*.dylib', prefix.lib)
        else:
            make('install-lib-shared', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
