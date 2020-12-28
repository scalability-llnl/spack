# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libunwind(AutotoolsPackage):
    """A portable and efficient C programming interface (API) to determine
       the call-chain of a program."""

    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"
    git      = "https://github.com/libunwind/libunwind"
    maintainers = ['mwkrentel']

    version('master', branch='master')
    version('1.5-head', branch='v1.5-stable')
    version('1.5-rc1', sha256='3e0cbc6dee326592097ef06e97cf76ef597987eddd0df8bea49b0594e587627a')
    version('1.4-head', branch='v1.4-stable')
    version('1.4.0',   sha256='df59c931bd4d7ebfd83ee481c943edf015138089b8e50abed8d9c57ba9338435', preferred=True)
    version('1.4-rc1', sha256='1928459139f048f9b4aca4bb5010540cb7718d44220835a2980b85429007fa9f')
    version('1.3.1', sha256='43997a3939b6ccdf2f669b50fdb8a4d3205374728c2923ddc2354c65260214f8')
    version('1.2.1', sha256='3f3ecb90e28cbe53fba7a4a27ccce7aad188d3210bb1964a923a731a27a75acb')
    version('1.1', sha256='9dfe0fcae2a866de9d3942c66995e4b460230446887dbdab302d41a8aee8d09a')

    variant('pic', default=False,
            description='Compile with position independent code.')

    variant('xz', default=False,
            description='Support xz (lzma) compressed symbol tables.')

    variant('zlib', default=False,
            description='Support zlib compressed symbol tables '
            '(1.5 and later).')

    # The libunwind releases contain the autotools generated files,
    # but the git repo snapshots do not.
    depends_on('autoconf', type='build', when='@master,1.4-head,1.5-head')
    depends_on('automake', type='build', when='@master,1.4-head,1.5-head')
    depends_on('libtool',  type='build', when='@master,1.4-head,1.5-head')
    depends_on('m4',       type='build', when='@master,1.4-head,1.5-head')

    depends_on('xz', type='link', when='+xz')
    depends_on('zlib', type='link', when='+zlib')

    conflicts('platform=darwin',
              msg='Non-GNU libunwind needs ELF libraries Darwin does not have')

    provides('unwind')

    def flag_handler(self, name, flags):
        wrapper_flags = []

        if name == 'cflags':
            # https://github.com/libunwind/libunwind/pull/166
            if self.spec.satisfies('@:1.4 %gcc@10:'):
                wrapper_flags.append('-fcommon')

            if '+pic' in self.spec:
                wrapper_flags.append(self.compiler.cc_pic_flag)

        return (wrapper_flags, None, flags)

    def configure_args(self):
        spec = self.spec
        args = []

        if '+xz' in spec:
            args.append('--enable-minidebuginfo')
        else:
            args.append('--disable-minidebuginfo')

        # zlib support is available in 1.5.x and later
        if spec.satisfies('@1.5:'):
            if '+zlib' in spec:
                args.append('--enable-zlibdebuginfo')
            else:
                args.append('--disable-zlibdebuginfo')

        return args
