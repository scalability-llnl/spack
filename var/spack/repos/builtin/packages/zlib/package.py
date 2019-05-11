# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
class Zlib(Package):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"

    version('1.2.11', '1c9f62f0778697a09d36121ead88e08e')
    # Due to the bug fixes, any installations of 1.2.9 or 1.2.10 should be
    # immediately replaced with 1.2.11.
    version('1.2.8', '44d667c142d7cda120332623eab69f40')
    version('1.2.3', 'debc62758716a169df9f62e6ab2bc634')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True,
            description='Enables the build of shared libraries.')
    variant('optimize', default=True,
            description='Enable -O2 for a more optimized lib')

    patch('w_patch.patch', when="@1.2.11%cce")

    # The following attribute is used by the default 'headers' handler.
    headers_names = ['zlib.h']

    # The following attribute is used by the default 'libs' handler.
    libs_names = ['libz']

    def setup_environment(self, spack_env, run_env):
        if '+pic' in self.spec:
            spack_env.append_flags('CFLAGS', self.compiler.pic_flag)
        if '+optimize' in self.spec:
            spack_env.append_flags('CFLAGS', '-O2')

    def install(self, spec, prefix):
        config_args = []
        if '~shared' in spec:
            config_args.append('--static')
        configure('--prefix={0}'.format(prefix), *config_args)

        make()
        if self.run_tests:
            make('check')
        make('install')
