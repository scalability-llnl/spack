# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ldak(Package):
    """LDAK is a software package for analyzing GWAS data"""

    homepage = "http://dougspeed.com/ldak/"
    url      = "http://dougspeed.com/wp-content/uploads/source.zip"

    version('5.1', sha256='9a3fe2fafc7b68cc57a17748a64db66f76b13acbd5e9a538ede20a46447fcf4a')

    variant('mkl', default=False, description='Use MKL')

    depends_on('zlib')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mkl', when='+mkl')

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
        if '+mkl' in spec:
            make('ldak')
            mkdirp(prefix.bin)
            install('ldak', prefix.bin)
        else:
            make('ldak_slow')
            mkdirp(prefix.bin)
            install('ldak_slow', prefix.bin.ldak)
