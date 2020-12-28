# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zstd(MakefilePackage):
    """Zstandard, or zstd as short version, is a fast lossless compression
    algorithm, targeting real-time compression scenarios at zlib-level and
    better compression ratios."""

    homepage = "http://facebook.github.io/zstd/"
    url      = "https://github.com/facebook/zstd/archive/v1.4.3.tar.gz"

    version('1.4.5', sha256='734d1f565c42f691f8420c8d06783ad818060fc390dee43ae0a89f86d0a4f8c2')
    version('1.4.4', sha256='a364f5162c7d1a455cc915e8e3cf5f4bd8b75d09bc0f53965b0c9ca1383c52c8')
    version('1.4.3', sha256='5eda3502ecc285c3c92ee0cc8cd002234dee39d539b3f692997a0e80de1d33de')
    version('1.4.2', sha256='7a6e1dad34054b35e2e847eb3289be8820a5d378228802239852f913c6dcf6a7')
    version('1.4.0', sha256='63be339137d2b683c6d19a9e34f4fb684790e864fee13c7dd40e197a64c705c1')
    version('1.3.8', sha256='90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3')
    version('1.3.0', sha256='0fdba643b438b7cbce700dcc0e7b3e3da6d829088c63757a5984930e2f70b348')
    version('1.1.2', sha256='980b8febb0118e22f6ed70d23b5b3e600995dbf7489c1f6d6122c1411cdda8d8')

    variant('pic', default=True, description='Build position independent code')

    depends_on('zlib')

    def setup_build_environment(self, env):
        if '+pic' in self.spec:
            env.append_flags('CFLAGS', self.compiler.cc_pic_flag)

    def build(self, spec, prefix):
        make('PREFIX={0}'.format(prefix))

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))

    def patch(self):
        # Remove flags not understood by the NVIDIA compilers
        if self.spec.satisfies('%nvhpc'):
            filter_file('-fvisibility=hidden', '', 'lib/Makefile')
            filter_file('-Wc++-compat', '', 'lib/Makefile', string=True)
            filter_file('-Wcast-align', '', 'lib/Makefile')
            filter_file('-Wcast-qual', '', 'lib/Makefile')
            filter_file('-Wdeclaration-after-statement', '', 'lib/Makefile')
            filter_file('-Wextra', '', 'lib/Makefile')
            filter_file('-Wfloat-equal', '', 'lib/Makefile')
            filter_file('-Wformat=2', '', 'lib/Makefile')
            filter_file('-Winit-self', '', 'lib/Makefile')
            filter_file('-Wmissing-prototypes', '', 'lib/Makefile')
            filter_file('-Wpointer-arith', '', 'lib/Makefile')
            filter_file('-Wredundant-decls', '', 'lib/Makefile')
            filter_file('-Wshadow', '', 'lib/Makefile')
            filter_file('-Wstrict-aliasing=1', '', 'lib/Makefile')
            filter_file('-Wstrict-prototypes', '', 'lib/Makefile')
            filter_file('-Wswitch-enum', '', 'lib/Makefile')
            filter_file('-Wundef', '', 'lib/Makefile')
            filter_file('-Wvla', '', 'lib/Makefile')
            filter_file('-Wwrite-strings', '', 'lib/Makefile')
