# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "http://www.libarchive.org"
    url      = "http://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    version('3.5.1', sha256='9015d109ec00bb9ae1a384b172bf2fc1dff41e2c66e5a9eeddf933af9db37f5a')
    version('3.4.1', sha256='fcf87f3ad8db2e4f74f32526dee62dd1fb9894782b0a503a89c9d7a70a235191')
    version('3.3.2', sha256='ed2dbd6954792b2c054ccf8ec4b330a54b85904a80cef477a1c74643ddafa0ce')
    version('3.2.1', sha256='72ee1a4e3fd534525f13a0ba1aa7b05b203d186e0c6072a8a4738649d0b3cfd2')
    version('3.1.2', sha256='eb87eacd8fe49e8d90c8fdc189813023ccc319c5e752b01fb6ad0cc7b2c53d5e')
    version('3.1.1', sha256='4968f9a3f2405ec7e07d5f6e78b36f21bceee6196df0a795165f89774bbbc6d8')
    version('3.1.0', sha256='64b15dfa623b323da8fc9c238b5bca962ec3b38dcdfd2ed86f5f509e578a3524')

    depends_on('zlib')
    depends_on('bzip2')
    depends_on('lz4')
    depends_on('xz')
    depends_on('lzo')
    depends_on('nettle')
    depends_on('openssl')
    depends_on('libxml2')
    depends_on('expat')

    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel
