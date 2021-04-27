# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Ldak(Package):
    """LDAK is a software package for analyzing GWAS data"""

    homepage = "http://dougspeed.com/ldak/"
    url      = "http://dougspeed.com/wp-content/uploads/source.zip"

    version('5.1', sha256='ae3eb8c2ef31af210e138336fd6edcd0e3a26ea9bae89fd6c0c6ea33e3a1517e')

    variant('mkl', default=False, description='Use MKL')

    depends_on('zlib')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mkl', when='+mkl')

    for t in ['aarch64', 'arm', 'ppc', 'ppc64', 'ppc64le',
              'ppcle', 'sparc', 'sparc64', 'x86']:
        conflicts('target={0}:'.format(t),
                  msg='libspot is available linux x86_64 only')

    def setup_build_environment(self, env):
        env.append_flags('LDLIBS', '-lm')
        env.append_flags('LDLIBS', '-lz')
        libs = (self.spec['lapack'].libs + self.spec['blas'].libs).ld_flags
        env.append_flags('LDLIBS', libs)
        if self.spec.platform == 'darwin':
            env.append_flags('LDLIBS', 'libqsopt.mac.a')
        else:
            env.append_flags('LDLIBS', 'libqsopt.linux.a')

    def install(self, spec, prefix):
        if self.spec.satisfies('~mkl'):
            filter_file('#define MKL.*', '#define MKL 0', 'ldak.c')
        make('ldak')
        mkdirp(prefix.bin)
        install('ldak', prefix.bin.ldak)
