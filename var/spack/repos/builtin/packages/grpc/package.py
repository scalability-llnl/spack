# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Grpc(CMakePackage):
    """A high performance, open-source universal RPC framework."""

    maintainers = ['nazavode']

    homepage = "https://grpc.io"
    url      = "https://github.com/grpc/grpc/archive/v1.30.0.tar.gz"

    version('1.30.0', sha256='419dba362eaf8f1d36849ceee17c3e2ff8ff12ac666b42d3ff02a164ebe090e9')
    version('1.29.1', sha256='0343e6dbde66e9a31c691f2f61e98d79f3584e03a11511fad3f10e3667832a45')
    version('1.29.0', sha256='c0a6b40a222e51bea5c53090e9e65de46aee2d84c7fa7638f09cb68c3331b983')
    version('1.28.2', sha256='4bec3edf82556b539f7e9f3d3801cba540e272af87293a3f4178504239bd111e')
    version('1.28.1', sha256='4cbce7f708917b6e58b631c24c59fe720acc8fef5f959df9a58cdf9558d0a79b')
    version('1.28.0', sha256='d6277f77e0bb922d3f6f56c0f93292bb4cfabfc3c92b31ee5ccea0e100303612')
    version('1.27.0', sha256='3ccc4e5ae8c1ce844456e39cc11f1c991a7da74396faabe83d779836ef449bce')
    version('1.26.0', sha256='2fcb7f1ab160d6fd3aaade64520be3e5446fc4c6fa7ba6581afdc4e26094bd81')
    version('1.25.0', sha256='ffbe61269160ea745e487f79b0fd06b6edd3d50c6d9123f053b5634737cf2f69')
    version('1.24.3', sha256='c84b3fa140fcd6cce79b3f9de6357c5733a0071e04ca4e65ba5f8d306f10f033')
    version('1.23.1', sha256='dd7da002b15641e4841f20a1f3eb1e359edb69d5ccf8ac64c362823b05f523d9')

    variant('shared', default=False,
            description='Build shared instead of static libraries')
    variant('codegen', default=True,
            description='Builds code generation plugins for protobuf '
                        'compiler (protoc)')

    depends_on('protobuf')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')
    depends_on('abseil-cpp', when='@1.27:')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:Bool={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF'),
            '-DgRPC_BUILD_CODEGEN:Bool={0}'.format(
                'ON' if '+codegen' in self.spec else 'OFF'),
            '-DgRPC_BUILD_CSHARP_EXT:Bool=OFF',
            '-DgRPC_INSTALL:Bool=ON',
            # Tell grpc to skip vendoring and look for deps via find_package:
            '-DgRPC_CARES_PROVIDER:String=package',
            '-DgRPC_ZLIB_PROVIDER:String=package',
            '-DgRPC_SSL_PROVIDER:String=package',
            '-DgRPC_PROTOBUF_PROVIDER:String=package',
            '-DgRPC_USE_PROTO_LITE:Bool=OFF',
            '-DgRPC_PROTOBUF_PACKAGE_TYPE:String=CONFIG',
            # Disable tests:
            '-DgRPC_BUILD_TESTS:BOOL=OFF',
            '-DgRPC_GFLAGS_PROVIDER:String=none',
            '-DgRPC_BENCHMARK_PROVIDER:String=none',
        ]
        if self.spec.satisfies('@1.27.0:'):
            args.append('-DgRPC_ABSL_PROVIDER:String=package')
        return args
