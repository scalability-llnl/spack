# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfuse(AutotoolsPackage):
    """squashfuse - Mount SquashFS archives using FUSE"""

    homepage = "https://github.com/vasi/squashfuse"
    url      = "https://github.com/vasi/squashfuse/releases/download/0.1.104/squashfuse-0.1.104.tar.gz"
    git      = "https://github.com/vasi/squashfuse.git"

    maintainers = ['haampie']

    version('master', branch='master')
    version('0.1.104', sha256='aa52460559e0d0b1753f6b1af5c68cfb777ca5a13913285e93f4f9b7aa894b3a')
    version('0.1.103', sha256='42d4dfd17ed186745117cfd427023eb81effff3832bab09067823492b6b982e7')

    variant('shared', default=True, description='Enable shared libraries')
    variant('static', default=True, description='Enable static libraries')
    variant('min_size', default=False, description='Build small binaries')

    variant('zlib', default=True, description='Enable zlib/gzip compression support')
    variant('lz4', default=True, description='Enable LZ4 compression support')
    variant('lzo', default=True, description='Enable LZO compression support')
    variant('xz', default=True, description='Enable xz compression support')
    variant('zstd', default=True, description='Enable Zstandard/zstd support')

    conflicts('~shared', when='~static', msg="Enable shared, static or both")

    depends_on('libfuse@2.5:')
    depends_on('libfuse@:2.99', when='@:0.1.103')

    # Note: typically libfuse is external, but this implies that you have to make
    # pkg-config external too, because spack's pkg-config doesn't know how to
    # locate system pkg-config's fuse.pc/fuse3.pc
    depends_on('pkgconfig', type='build')

    # compression libs
    depends_on('zlib', when='+zlib')
    depends_on('lz4', when='+lz4')
    depends_on('lzo', when='+lzo')
    depends_on('xz', when='+xz')
    depends_on('zstd', when='+zstd')

    depends_on('m4',       type='build', when='@master')
    depends_on('autoconf', type='build', when='@master')
    depends_on('automake', type='build', when='@master')
    depends_on('libtool',  type='build', when='@master')

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+min_size' in self.spec:
            if '-Os' in self.compiler.opt_flags:
                flags.append('-Os')
                return (None, None, flags)

        return (flags, None, None)

    def configure_args(self):
        args = ['--disable-demo']
        args += self.enable_or_disable('shared')
        args += self.enable_or_disable('static')
        args += self.with_or_without('zlib', activation_value='prefix')
        args += self.with_or_without('lz4', activation_value='prefix')
        args += self.with_or_without('lzo', activation_value='prefix')
        args += self.with_or_without('xz', activation_value='prefix')
        args += self.with_or_without('zstd', activation_value='prefix')
        return args
