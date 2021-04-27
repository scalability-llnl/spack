# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfs(MakefilePackage):
    """Squashfs - read only compressed filesystem"""

    homepage = 'http://squashfs.sourceforge.net'
    url      = 'https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz'

    # version      sha1
    version('4.4', sha256='a981b3f3f2054b5a2e658851a3c06a2460ad04a9a8a645e0afe063a63fdbb07e')
    version('4.3', sha256='0d605512437b1eb800b4736791559295ee5f60177e102e4d4ccd0ee241a5f3f6')
    version('4.2', sha256='d9e0195aa922dbb665ed322b9aaa96e04a476ee650f39bbeadb0d00b24022e96')
    version('4.1', sha256='3a870d065a25b3f5467bc6d9ed34340befab51a3f9e4b7e3792ea0ff4e06046a')
    version('4.0', sha256='18948edbe06bac2c4307eea99bfb962643e4b82e5b7edd541b4d743748e12e21')

    variant('gzip', default=True, description='Enable gzip compression support')
    variant('lz4', default=False, description='Enable LZ4 compression support')
    variant('lzo', default=False, description='Enable LZO compression support')
    variant('xz', default=False, description='Enable xz compression support')
    variant('zstd', default=False, description='Enable Zstandard/zstd support')
    variant('default_compression', default='gzip', values=('gzip', 'lz4', 'lzo', 'xz', 'zstd'),
            multi=False, description='Default compression algorithm')

    conflicts('squashfs~gzip default_compression=gzip', msg='Cannot set default compression to missing algorithm')
    conflicts('squashfs~lz4 default_compression=lz4', msg='Cannot set default compression to missing algorithm')
    conflicts('squashfs~lzo default_compression=lzo', msg='Cannot set default compression to missing algorithm')
    conflicts('squashfs~xz default_compression=xz', msg='Cannot set default compression to missing algorithm')
    conflicts('squashfs~zstd default_compression=zstd', msg='Cannot set default compression to missing algorithm')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    depends_on('zlib', when='+gzip')
    depends_on('lz4', when='+lz4')
    depends_on('lzo', when='+lzo')
    depends_on('xz', when='+xz')
    depends_on('zstd', when='+zstd')

    # patch from
    # https://github.com/plougher/squashfs-tools/commit/fe2f5da4b0f8994169c53e84b7cb8a0feefc97b5.patch
    patch('gcc-10.patch', when="%gcc@10:")
    patch('gcc-10.patch', when="%clang@11:")

    def make_options(self, spec):
        default = spec.variants['default_compression'].value
        return [
            'GZIP_SUPPORT={0}'.format(1 if '+gzip' in spec else 0),
            'LZ4_SUPPORT={0}' .format(1 if '+lz4'  in spec else 0),
            'LZO_SUPPORT={0}' .format(1 if '+lzo'  in spec else 0),
            'XZ_SUPPORT={0}'  .format(1 if '+xz'   in spec else 0),
            'ZSTD_SUPPORT={0}'.format(1 if '+zstd' in spec else 0),
            'COMP_DEFAULT={0}'.format(default),
        ]

    def build(self, spec, prefix):
        options = self.make_options(spec)
        with working_dir('squashfs-tools'):
            make(*options, parallel=False)

    def install(self, spec, prefix):
        options = self.make_options(spec)
        with working_dir('squashfs-tools'):
            make('install', 'INSTALL_DIR=%s' % prefix.bin, *options, parallel=False)
