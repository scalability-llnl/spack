# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibjpegTurbo(Package):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
    accelerate baseline JPEG compression and decompression.

    libjpeg is a library that implements JPEG image encoding, decoding and
    transcoding.
    """
    # https://github.com/libjpeg-turbo/libjpeg-turbo/blob/master/BUILDING.md
    homepage = "https://libjpeg-turbo.org/"
    url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/2.0.3.tar.gz"

    version('2.0.4', sha256='7777c3c19762940cff42b3ba4d7cd5c52d1671b39a79532050c85efb99079064')
    version('2.0.3', sha256='a69598bf079463b34d45ca7268462a18b6507fdaa62bb1dfd212f02041499b5d')
    version('2.0.2', sha256='b45255bd476c19c7c6b198c07c0487e8b8536373b82f2b38346b32b4fa7bb942')
    version('1.5.90', sha256='cb948ade92561d8626fd7866a4a7ba3b952f9759ea3dd642927bc687470f60b7')
    version('1.5.3', sha256='1a17020f859cb12711175a67eab5c71fc1904e04b587046218e36106e07eabde')
    version('1.5.0', sha256='232280e1c9c3e6a1de95fe99be2f7f9c0362ee08f3e3e48d50ee83b9a2ed955b')
    version('1.3.1', sha256='5008aeeac303ea9159a0ec3ccff295434f4e63b05aed4a684c9964d497304524')

    provides('jpeg')

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on('yasm', type='build')
    depends_on('nasm', type='build')
    depends_on('autoconf', type='build', when='@1.3.1:1.5.3')
    depends_on('automake', type='build', when='@1.3.1:1.5.3')
    depends_on('libtool', type='build', when='@1.3.1:1.5.3')
    depends_on('cmake', type='build', when='@1.5.90:')

    @property
    def libs(self):
        return find_libraries('libjpeg*', root=self.prefix, recursive=True)

    def flag_handler(self, name, flags):
        if self.spec.satisfies('@1.5.90:'):
            return (None, None, flags)
        else:
            # compiler flags for earlier version are injected into the
            # spack compiler wrapper
            return (flags, None, None)

    def flags_to_build_system_args(self, flags):
        # This only handles cflags, other flags are discarded
        cmake_flag_args = []
        if 'cflags' in flags and flags['cflags']:
            cmake_flag_args.append('-DCMAKE_C_FLAGS={0}'.format(
                                   ' '.join(flags['cflags'])))
        self.cmake_flag_args = cmake_flag_args

    @when('@1.3.1:1.5.3')
    def install(self, spec, prefix):
        autoreconf('-ifv')
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    @when('@1.5.90:')
    def install(self, spec, prefix):
        cmake_args = ['-GUnix Makefiles']
        if hasattr(self, 'cmake_flag_args'):
            cmake_args.extend(self.cmake_flag_args)
        cmake_args.extend(std_cmake_args)
        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')
