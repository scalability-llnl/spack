# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbson(Package):
    """libbson is a library providing useful routines related to building,
    parsing, and iterating BSON documents."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url      = "https://github.com/mongodb/mongo-c-driver/releases/download/1.16.2/mongo-c-driver-1.16.2.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.17.0', sha256='90aa23a3f92be0a076fe0b903b68276a7973d4e472929943069f503d5ab50cb9')
    version('1.16.2', sha256='0a722180e5b5c86c415b9256d753b2d5552901dc5d95c9f022072c3cd336887e')
    version('1.9.5', sha256='6bb51b863a4641d6d7729e4b55df8f4389ed534c34eb3a1cda906a53df11072c')
    version('1.9.4', sha256='c3cc230a3451bf7fedc5bb34c3191fd23d841e65ec415301f6c77e531924b769')
    version('1.9.3', sha256='244e786c746fe6326433b1a6fcaadbdedc0da3d11c7b3168f0afa468f310e5f1')
    version('1.9.1', sha256='236d9fcec0fe419c2201481081e497f49136eda2349b61cfede6233013bf7601')
    version('1.8.1', sha256='9d18d14671b7890e27b2a5ce33a73a5ed5d33d39bba70209bae99c1dc7aa1ed4')
    version('1.8.0', sha256='63dea744b265a2e17c7b5e289f7803c679721d98e2975ea7d56bc1e7b8586bc1')
    version('1.7.0', sha256='442d89e89dfb43bba1f65080dc61fdcba01dcb23468b2842c1dbdd4acd6049d3')
    version('1.6.3', sha256='e9e4012a9080bdc927b5060b126a2c82ca11e71ebe7f2152d079fa2ce461a7fb')
    version('1.6.2', sha256='aad410123e4bd8a9804c3c3d79e03344e2df104872594dc2cf19605d492944ba')
    version('1.6.1', sha256='5f160d44ea42ce9352a7a3607bc10d3b4b22d3271763aa3b3a12665e73e3a02d')

    depends_on('cmake@3.1:', type='build', when='@1.10.0:')

    depends_on('autoconf', type='build', when='@1.6.1')
    depends_on('automake', type='build', when='@1.6.1')
    depends_on('libtool', type='build', when='@1.6.1')
    depends_on('m4', type='build', when='@1.6.1')

    def url_for_version(self, version):
        if version >= Version('1.10.0'):
            url = 'https://github.com/mongodb/mongo-c-driver/releases/download/{0}/mongo-c-driver-{0}.tar.gz'
        else:
            url = 'https://github.com/mongodb/libbson/releases/download/{0}/libbson-{0}.tar.gz'

        return url.format(version)

    def cmake_args(self):
        args = [
            '-DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF',
            '-DENABLE_MONGOC=OFF'
        ]

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
        # 1.6.1 tarball is broken
        return self.spec.satisfies('@1.6.1')

    @when('@:1.9.99')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
