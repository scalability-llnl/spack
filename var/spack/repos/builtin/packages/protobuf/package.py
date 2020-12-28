# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import spack.util.web
from spack.package import *


class Protobuf(Package):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url      = "https://github.com/protocolbuffers/protobuf/archive/v3.12.2.tar.gz"

    version('3.12.2',  sha256='bb8ce9ba11eb7bccf080599fe7cad9cc461751c8dd1ba61701c0070d58cde973')
    version('3.12.1',  sha256='cb9b3f9d625b5739a358268eb3421de11cacd90025f5f7672c3930553eca810e')
    version('3.12.0',  sha256='946ba5371e423e1220d2cbefc1f65e69a1e81ca5bab62a03d66894172983cfcd')
    version('3.11.4',  sha256='a79d19dcdf9139fa4b81206e318e33d245c4c9da1ffed21c87288ed4380426f9')
    version('3.11.3',  sha256='cf754718b0aa945b00550ed7962ddc167167bd922b842199eeb6505e6f344852')
    version('3.11.2',  sha256='e8c7601439dbd4489fe5069c33d374804990a56c2f710e00227ee5d8fd650e67')
    version('3.11.1',  sha256='4f8e805825c53bbc3c9f6b6abc009b5b5679e4702bccfca1121c42ff5ec801c7')
    version('3.11.0',  sha256='6d356a6279cc76d2d5c4dfa6541641264b59eae0bc96b852381361e3400d1f1c')
    version('3.10.1',  sha256='6adf73fd7f90409e479d6ac86529ade2d45f50494c5c10f539226693cb8fe4f7')
    version('3.10.0',  sha256='758249b537abba2f21ebc2d02555bf080917f0f2f88f4cbe2903e0e28c4187ed')
    version('3.9.2',   sha256='1fbf1c2962af287607232b2eddeaec9b4f4a7a6f5934e1a9276e9af76952f7e0')
    version('3.9.1',   sha256='98e615d592d237f94db8bf033fba78cd404d979b0b70351a9e5aaff725398357')
    version('3.7.1',   sha256='f1748989842b46fa208b2a6e4e2785133cfcc3e4d43c17fecb023733f0f5443f')
    version('3.7.0',   sha256='a19dcfe9d156ae45d209b15e0faed5c7b5f109b6117bfc1974b6a7b98a850320')
    version('3.6.1',   sha256='3d4e589d81b2006ca603c1ab712c9715a76227293032d05b26fca603f90b3f5b')
    version('3.5.2',   sha256='4ffd420f39f226e96aebc3554f9c66a912f6cad6261f39f194f16af8a1f6dab2')
    version('3.5.1.1', sha256='56b5d9e1ab2bf4f5736c4cfba9f4981fbc6976246721e7ded5602fbaee6d6869')
    version('3.5.1',   sha256='826425182ee43990731217b917c5c3ea7190cfda141af4869e6d4ad9085a740f')
    version('3.5.0.1', sha256='86be71e61c76575c60839452a4f265449a6ea51570d7983cb929f06ad294b5f5')
    version('3.5.0',   sha256='0cc6607e2daa675101e9b7398a436f09167dffb8ca0489b0307ff7260498c13c')
    version('3.4.1',   sha256='8e0236242106e680b4f9f576cc44b8cd711e948b20a9fc07769b0a20ceab9cc4')
    version('3.4.0',   sha256='f6600abeee3babfa18591961a0ff21e7db6a6d9ef82418a261ec4fee44ee6d44')
    version('3.3.0',   sha256='9a36bc1265fa83b8e818714c0d4f08b8cec97a1910de0754a321b11e66eb76de')
    version('3.2.0',   sha256='a839d3f1519ff9d68ab908de5a0f269650ef1fc501c10f6eefd4cae51d29b86f')
    version('3.1.0',   sha256='fb2a314f4be897491bb2446697be693d489af645cb0e165a85e7e64e07eb134d')
    version('3.0.2',   sha256='a0a265bcc9d4e98c87416e59c33afc37cede9fb277292523739417e449b18c1e')
    version('2.5.0',   sha256='c2665a7aa2ac1a206e61b28e014486e3de59009ea2be2bde9182e0847f38b62f')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('cmake', when='@3.0.2:', type='build')
    depends_on('zlib')
    depends_on('autoconf', type='build', when='@2.5.0')
    depends_on('automake', type='build', when='@2.5.0')
    depends_on('libtool',  type='build', when='@2.5.0')
    depends_on('m4',       type='build', when='@2.5.0')

    conflicts('%gcc@:4.6', when='@3.6.0:')  # Requires c++11
    conflicts('%gcc@:4.6', when='@3.2.0:3.3.0')  # Breaks

    # first fixed in 3.4.0: https://github.com/google/protobuf/pull/3406
    patch('pkgconfig.patch', when='@3.0.2:3.3.2')

    patch('intel-v1.patch', when='@3.2:3.6 %intel')

    # See https://github.com/protocolbuffers/protobuf/pull/7197
    patch('intel-v2.patch', when='@3.7:3.11.4 %intel')

    patch('protoc2.5.0_aarch64.patch', sha256='7b44fcdb794f421174d619f83584e00a36012a16da09079e2fad9c12f7337451', when='@2.5.0 target=aarch64:')

    def fetch_remote_versions(self):
        """Ignore additional source artifacts uploaded with releases,
           only keep known versions
           fix for https://github.com/spack/spack/issues/5356"""
        return dict(map(
            lambda u: (u, self.url_for_version(u)),
            spack.util.web.find_versions_of_archive(
                self.all_urls, self.list_url, self.list_depth)
        ))

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS=%s' % int('+shared' in self.spec),
            '-Dprotobuf_BUILD_TESTS:BOOL=OFF',
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON'
        ]
        if sys.platform == 'darwin':
            args.extend(['-DCMAKE_MACOSX_RPATH=ON'])
        return args

    @when('@3.0.2:')
    def install(self, spec, prefix):
        args = self.cmake_args()
        args.extend(std_cmake_args)

        source_directory = join_path(self.stage.source_path, 'cmake')
        build_directory = join_path(source_directory, 'build')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *args)
            make()
            make('install')

    def configure_args(self):
        args = []
        args.append('--prefix=%s' % self.prefix)
        return args

    @when('@2.5.0')
    def install(self, spec, prefix):
        args = self.configure_args()
        autoreconf('-ifv')
        configure(*args)
        make()
        make('install')
