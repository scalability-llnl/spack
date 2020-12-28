# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MongoCDriver(Package):
    """libmongoc is a client library written in C for MongoDB."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url      = "https://github.com/mongodb/mongo-c-driver/releases/download/1.7.0/mongo-c-driver-1.7.0.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.17.0', sha256='90aa23a3f92be0a076fe0b903b68276a7973d4e472929943069f503d5ab50cb9')
    version('1.16.2', sha256='0a722180e5b5c86c415b9256d753b2d5552901dc5d95c9f022072c3cd336887e')
    version('1.9.5', sha256='4a4bd0b0375450250a3da50c050b84b9ba8950ce32e16555714e75ebae0b8019')
    version('1.9.4', sha256='910c2f1b2e3df4d0ea39c2f242160028f90fcb8201f05339a730ec4ba70811fb')
    version('1.9.3', sha256='c2c94ef63aaa09efabcbadc4ac3c8740faa102266bdd2559d550f1955b824398')
    version('1.9.1', sha256='91951444d34581deeaff46cc2985c68805754f618a20ac369b761ce9b621c4cd')
    version('1.8.1', sha256='87d87b7581018cde7edff85f522d43d9c0a226df26fa53b77ca1613a3aca8233')
    version('1.8.0', sha256='1b53883b4cbf08e7d77ad7ab7a02deca90b1719c67f9ad132b47e60d0206ea4e')
    version('1.7.0', sha256='48a0dbd44fef2124b51cf501f06be269b1a39452303b880b37473a6030c6e023')
    version('1.6.3', sha256='82df03de117a3ccf563b9eccfd2e5365df8f215a36dea7446d439969033ced7b')
    version('1.6.2', sha256='7ec27e9be4da2bf9e4b316374f8c29f816f0a0f019b984411777e9681e17f70e')
    version('1.6.1', sha256='1bdfb27944c6da8e56da209a5d56efac70df1f8c4ca4498b46f75bf3f9360898')

    variant('ssl', default=True, description='Enable SSL support.')
    variant('snappy', default=True, description='Enable Snappy support.')
    variant('zlib', default=True, description='Enable zlib support.')
    variant('zstd', default=True, description='Enable zstd support.')

    patch('https://github.com/mongodb/mongo-c-driver/pull/466.patch', sha256='713a872217d11aba04a774785a2824d26b566543c270a1fa386114f5200fda20', when='@1.8.1')

    depends_on('cmake@3.1:', type='build', when='@1.10.0:')

    depends_on('autoconf', type='build', when='@1.8.1')
    depends_on('automake', type='build', when='@1.8.1')
    depends_on('libtool', type='build', when='@1.8.1')
    depends_on('m4', type='build', when='@1.8.1')

    depends_on('pkgconfig', type='build')

    # When updating mongo-c-driver, libbson has to be kept in sync.
    depends_on('libbson@1.17.0:1.17.99', when='@1.17')
    depends_on('libbson@1.16.0:1.16.99', when='@1.16')
    depends_on('libbson@1.9.0:1.9.99', when='@1.9')
    depends_on('libbson@1.8.0:1.8.99', when='@1.8')
    depends_on('libbson@1.7.0:1.7.99', when='@1.7')
    depends_on('libbson@1.6.0:1.6.99', when='@1.6')

    depends_on('openssl', when='+ssl')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')
    depends_on('zstd', when='+zstd')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF',
            '-DENABLE_BSON=SYSTEM'
        ]

        if '+ssl' in spec:
            args.append('-DENABLE_SSL=OPENSSL')
        else:
            args.append('-DENABLE_SSL=OFF')

        if '+snappy' in spec:
            args.append('-DENABLE_SNAPPY=ON')
        else:
            args.append('-DENABLE_SNAPPY=OFF')

        if '+zlib' in spec:
            args.append('-DENABLE_ZLIB=SYSTEM')
        else:
            args.append('-DENABLE_ZLIB=OFF')

        if '+zstd' in spec:
            args.append('-DENABLE_ZSTD=ON')
        else:
            args.append('-DENABLE_ZSTD=OFF')

        return args

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            # We cannot simply do
            #   cmake('..', *std_cmake_args, *self.cmake_args())
            # because that is not Python 2 compatible. Instead, collect
            # arguments into a temporary buffer first.
            args = []
            args.extend(std_cmake_args)
            args.extend(self.cmake_args())
            cmake('..', *args)
            make()
            make('install')

    @property
    def force_autoreconf(self):
        # Run autoreconf due to build system patch
        return self.spec.satisfies('@1.8.1')

    def configure_args(self):
        spec = self.spec

        args = [
            '--disable-automatic-init-and-cleanup',
            '--with-libbson=system'
        ]

        if '+ssl' in spec:
            args.append('--enable-ssl=openssl')
        else:
            args.append('--enable-ssl=no')

        if spec.satisfies('@1.7.0:'):
            # --with-{snappy,zlib}=system are broken for versions < 1.8.1
            if '+snappy' not in spec:
                args.append('--with-snappy=no')
            elif spec.satisfies('@1.8.1:'):
                args.append('--with-snappy=system')

            if '+zlib' not in spec:
                args.append('--with-zlib=no')
            elif spec.satisfies('@1.8.1:'):
                args.append('--with-zlib=system')

        return args

    @when('@:1.9.99')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix), *self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
