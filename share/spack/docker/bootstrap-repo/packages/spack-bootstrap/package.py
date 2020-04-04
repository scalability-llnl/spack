# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# flake8: noqa

from spack import *


class SpackBootstrap(BundlePackage):
    # bootstrap phase 1
    version('1.0')
    depends_on('tar', when='@1')
    depends_on('xz', when='@1')

    # bootstrap phase 2
    version('2.0')
    depends_on('gzip', when='@2')
    depends_on('patch', when='@2')
    depends_on('sed', when='@2')
    depends_on('unzip', when='@2')

    # bootstrap phase 3
    version('3.0')
    depends_on('gcc @9.2.0 +strip languages=c,c++,fortran', when='@3')

    # bootstrap phase 4
    version('4.0')
    depends_on('git', when='@4')

    # bootstrap phase 5
    version('5.0')
    depends_on('autoconf', when='@5')
    depends_on('automake', when='@5')
    depends_on('binutils', when='@5')
    depends_on('bzip2', when='@5')
    depends_on('cmake @3.15.5 -ncurses -qt', when='@5')
    depends_on('coreutils', when='@5')
    depends_on('curl', when='@5')
    depends_on('diffutils', when='@5')
    depends_on('environment-modules', when='@5')
    depends_on('file', when='@5')
    depends_on('git', when='@5')
    depends_on('gmake', when='@5')
    depends_on('gnupg', when='@5')
    depends_on('grep', when='@5')
    depends_on('gzip', when='@5')
    depends_on('m4', when='@5')
    depends_on('nano', when='@5')
    depends_on('patch', when='@5')
    depends_on('patchelf', when='@5')
    depends_on('procps', when='@5')
    depends_on('py-boto3', when='@5')
    depends_on('py-pip', when='@5')
    depends_on('python @3.7.4'
            ' +bz2'
            ' +ctypes'
            ' +dbm'
            ' +lzma'
            ' +optimizations'
            ' +pic'
            ' +pyexpat'
            ' +pythoncmd'
            ' +readline'
            ' +sqlite3'
            ' +ssl'
            ' +uuid'
            ' +zlib', when='@5')
    depends_on('sed', when='@5')
    depends_on('tar', when='@5')
    depends_on('tcl', when='@5')
    depends_on('unzip', when='@5')
    depends_on('xz', when='@5')
    depends_on('zlib', when='@5')
