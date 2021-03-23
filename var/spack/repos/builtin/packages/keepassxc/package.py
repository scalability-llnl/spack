# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Keepassxc(CMakePackage):
    """KeePassXC - Cross-Platform Password Manager, modern, secure, and open-source."""

    homepage = "https://keepassxc.org"
    url      = "https://github.com/keepassxreboot/keepassxc/releases/download/2.6.4/keepassxc-2.6.4-src.tar.xz"
    git      = "https://github.com/keepassxreboot/keepassxc.git"

    maintainers = ['cessenat']

    version('master', branch='master')
    version('2.6.4', sha256='e536e2a71c90fcf264eb831fb1a8b518ee1b03829828f862eeea748d3310f82b')

    variant('build_type', default='Release',
            description='The build type for the installation (only Debug or'
            ' ( Documentation indicates Release).',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('autotype', default=False,
            description='enable auto-type')

    # https://github.com/keepassxreboot/keepassxc/wiki/Building-KeePassXC
    # https://github.com/keepassxreboot/keepassxc/wiki/Set-up-Build-Environment-on-Linux
    depends_on('cmake@3.1:', type='build')

    # It installs the last gcc instead of using one that is >= 4.7
    conflicts('%gcc@:4.7', when='%gcc',
              msg="Older than 4.7 GCC compilers are not supported")
    conflicts('%clang@:3.0', when='%clang',
              msg="Older than 3.0 clang compilers are not supported")

    # The following libraries are required:
    depends_on('qt+dbus~framework@5.2:')
    depends_on('libgcrypt@1.6:', type='link')
    depends_on('zlib', type='link')
    depends_on('libmicrohttpd', type='link')
    depends_on('libsodium@1.0.12:', type='link')
    depends_on('readline')
    # Modified argon2 on CentOS to have a standard library directory
    depends_on('argon2', type=('link', 'build'))
    # Had to add libqrencode
    depends_on('libqrencode', type=('link', 'build'))
    # Has anyone done gem i bundler and gem i asciidoctor ? https://asciidoctor.org/
    depends_on('ruby-asciidoctor@2.0:', type=('build'))
    # sudo apt install libxi-dev libxtst-dev libqt5x11extras5-dev libyubikey-dev \
    # libykpers-1-dev libquazip5-dev libreadline-dev
    # These are required to build Auto-Type, Yubikey and browser integration support.
    depends_on('libxi', type='link', when='+autotype')
    depends_on('libxtst', type='link', when='+autotype')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DKEEPASSXC_BUILD_TYPE=Release',
            '-DCMAKE_INSTALL_DATADIR=%s' % join_path(spec.prefix, 'share'),
        ]
        if '+autotype' in spec:
            args.append('-DWITH_XC_ALL=ON')
        else:
            args.append('-DWITH_XC_ALL=OFF')

        if spec.satisfies('platform=darwin'):
            args.append('-DCMAKE_OSX_ARCHITECTURES=x86_64')

        return args

    @when('platform=darwin')
    def make(self, spec, prefix):
        make('package')

    def edit(self, spec, prefix):
        env['DESTDIR'] = spec.prefix
