# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zstd(CMakePackage):
    """Zstandard, or zstd as short version, is a fast lossless compression
    algorithm, targeting real-time compression scenarios at zlib-level and
    better compression ratios."""

    homepage = "http://facebook.github.io/zstd/"
    url      = "https://github.com/facebook/zstd/archive/v1.4.3.tar.gz"
    git      = "https://github.com/facebook/zstd.git"

    root_cmakelists_dir = 'build/cmake'

    maintainers = ['haampie']

    version('develop', branch='dev')
    version('1.4.9', sha256='acf714d98e3db7b876e5b540cbf6dee298f60eb3c0723104f6d3f065cd60d6a8')
    version('1.4.8', sha256='f176f0626cb797022fbf257c3c644d71c1c747bb74c32201f9203654da35e9fa')
    version('1.4.7', sha256='085500c8d0b9c83afbc1dc0d8b4889336ad019eba930c5d6a9c6c86c20c769c8')
    version('1.4.5', sha256='734d1f565c42f691f8420c8d06783ad818060fc390dee43ae0a89f86d0a4f8c2')
    version('1.4.4', sha256='a364f5162c7d1a455cc915e8e3cf5f4bd8b75d09bc0f53965b0c9ca1383c52c8')
    version('1.4.3', sha256='5eda3502ecc285c3c92ee0cc8cd002234dee39d539b3f692997a0e80de1d33de')
    version('1.4.2', sha256='7a6e1dad34054b35e2e847eb3289be8820a5d378228802239852f913c6dcf6a7')
    version('1.4.0', sha256='63be339137d2b683c6d19a9e34f4fb684790e864fee13c7dd40e197a64c705c1')
    version('1.3.8', sha256='90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3')
    version('1.3.0', sha256='0fdba643b438b7cbce700dcc0e7b3e3da6d829088c63757a5984930e2f70b348')
    version('1.1.2', sha256='980b8febb0118e22f6ed70d23b5b3e600995dbf7489c1f6d6122c1411cdda8d8')

    variant('shared', default=True, description='Build shared libraries')
    variant('static', default=True, description='Build static libraries')
    variant('programs', default=True, description='Build executables')
    variant('legacy', default=False, description='Enable legacy support')
    variant('zlib', default=False, description='Build programs with zlib support')
    variant('lzma', default=False, description='Build programs with lzma support')
    variant('lz4', default=False, description='Build programs with zlib support')
    variant('multithread', default=True, description='Build with pthread support')

    conflicts('+zlib', when='~programs', msg="zlib requires programs to be built")
    conflicts('+lzma', when='~programs', msg="lzma requires programs to be built")
    conflicts('+lz4', when='~programs', msg="lz4 requires programs to be built")

    depends_on('zlib', when='+zlib')
    depends_on('lzma', when='+lzma')
    depends_on('lz4', when='+lz4')

    def cmake_args(self):
        return [
            self.define_from_variant('ZSTD_BUILD_PROGRAMS', 'programs'),
            self.define_from_variant('ZSTD_BUILD_STATIC', 'static'),
            self.define_from_variant('ZSTD_BUILD_SHARED', 'shared'),
            self.define_from_variant('ZSTD_LEGACY_SUPPORT', 'legacy'),
            self.define_from_variant('ZSTD_MULTITHREAD_SUPPORT', 'multithread')
        ]
