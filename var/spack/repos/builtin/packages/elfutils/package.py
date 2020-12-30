# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os.path


class Elfutils(AutotoolsPackage, SourcewarePackage):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"
    sourceware_mirror_path = "elfutils/0.179/elfutils-0.179.tar.bz2"
    list_url = "https://sourceware.org/elfutils/ftp"
    list_depth = 1

    version('0.182', sha256='ecc406914edf335f0b7fc084ebe6c460c4d6d5175bfdd6688c1c78d9146b8858')
    version('0.181', sha256='29a6ad7421ec2acfee489bb4a699908281ead2cb63a20a027ce8804a165f0eb3')
    version('0.180', sha256='b827b6e35c59d188ba97d7cf148fa8dc6f5c68eb6c5981888dfdbb758c0b569d')
    version('0.179', sha256='25a545566cbacaa37ae6222e58f1c48ea4570f53ba991886e2f5ce96e22a23a2')
    version('0.178', sha256='31e7a00e96d4e9c4bda452e1f2cdac4daf8abd24f5e154dee232131899f3a0f2')
    version('0.177', sha256='fa489deccbcae7d8c920f60d85906124c1989c591196d90e0fd668e3dc05042e')
    version('0.176', sha256='eb5747c371b0af0f71e86215a5ebb88728533c3a104a43d4231963f308cd1023')
    version('0.175', sha256='f7ef925541ee32c6d15ae5cb27da5f119e01a5ccdbe9fe57bf836730d7b7a65b')
    version('0.174', sha256='cdf27e70076e10a29539d89e367101d516bc4aa11b0d7777fe52139e3fcad08a')
    version('0.173', sha256='b76d8c133f68dad46250f5c223482c8299d454a69430d9aa5c19123345a000ff')
    version('0.170', sha256='1f844775576b79bdc9f9c717a50058d08620323c1e935458223a12f249c9e066')
    version('0.168', sha256='b88d07893ba1373c7dd69a7855974706d05377766568a7d9002706d5de72c276')
    version('0.163', sha256='7c774f1eef329309f3b05e730bdac50013155d437518a2ec0e24871d312f2e23')

    # Libraries for reading compressed DWARF sections.
    variant('bzip2', default=False,
            description='Support bzip2 compressed sections.')
    variant('xz', default=False,
            description='Support xz (lzma) compressed sections.')

    # Native language support from libintl.
    variant('nls', default=True,
            description='Enable Native Language Support.')

    # libdebuginfod support
    # NB: For 0.181 and newer, this enables _both_ the client and server
    variant('debuginfod', default=False,
            description='Enable libdebuginfod support.')

    depends_on('bzip2', type='link', when='+bzip2')
    depends_on('xz',    type='link', when='+xz')
    depends_on('zlib',  type='link')
    depends_on('gettext', when='+nls')
    depends_on('m4',    type='build')

    # debuginfod has extra dependencies
    # NB: Waiting on an elfutils patch before we can use libmicrohttpd@0.9.71
    depends_on('libmicrohttpd@0.9.33:0.9.70', type='link', when='+debuginfod')
    depends_on('libarchive@3.1.2:', type='link', when='+debuginfod')
    depends_on('sqlite@3.7.17:', type='link', when='+debuginfod')
    depends_on('curl@7.29.0:', type='link', when='+debuginfod')

    conflicts('%gcc@7.2.0:', when='@0.163')
    conflicts('+debuginfod', when='@:0.178')

    provides('elf@1')

    # Elfutils uses nested functions in C code, which is implemented
    # in gcc, but not in clang. C code compiled with gcc is
    # binary-compatible with clang, so it should be possible to build
    # elfutils with gcc, and then link it to clang-built libraries.
    conflicts('%apple-clang')
    conflicts('%clang')

    # Elfutils uses -Wall and we don't want to fail the build over a
    # stray warning.
    def patch(self):
        files = glob.glob(os.path.join('*', 'Makefile.in'))
        filter_file('-Werror', '', *files)

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec
        args = []

        if '+bzip2' in spec:
            args.append('--with-bzlib=%s' % spec['bzip2'].prefix)
        else:
            args.append('--without-bzlib')

        if '+xz' in spec:
            args.append('--with-lzma=%s' % spec['xz'].prefix)
        else:
            args.append('--without-lzma')

        # zlib is required
        args.append('--with-zlib=%s' % spec['zlib'].prefix)

        if '+nls' in spec:
            # configure doesn't use LIBS correctly
            if self.spec['gettext'].prefix != '/usr':
                args.append('LDFLAGS=-Wl,--no-as-needed -L%s -lintl' %
                            spec['gettext'].prefix.lib)
        else:
            args.append('--disable-nls')

        if '+debuginfod' in spec:
            args.append('--enable-debuginfod')
            if spec.satisfies('@0.181:'):
                args.append('--enable-libdebuginfod')
        else:
            args.append('--disable-debuginfod')
            if spec.satisfies('@0.181:'):
                args.append('--disable-libdebuginfod')

        return args

    # Install elf.h to include directory.
    @run_after('install')
    def install_elfh(self):
        install(join_path('libelf', 'elf.h'), self.prefix.include)

    # Provide location of libelf.so to match libelf.
    @property
    def libs(self):
        return find_libraries('libelf', self.prefix, recursive=True)
