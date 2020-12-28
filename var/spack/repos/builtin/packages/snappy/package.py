# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snappy(CMakePackage):
    """A fast compressor/decompressor: https://code.google.com/p/snappy"""

    homepage = "https://github.com/google/snappy"
    url      = "https://github.com/google/snappy/archive/1.1.8.tar.gz"

    version('1.1.8', sha256='16b677f07832a612b0836178db7f374e414f94657c138e6993cbfc5dcc58651f')
    version('1.1.7', sha256='3dfa02e873ff51a11ee02b9ca391807f0c8ea0529a4924afa645fbf97163f9d4')

    variant('shared', default=True, description='Build shared libraries')
    variant('pic', default=True, description='Build position independent code')

    depends_on('googletest', type='test')

    patch('link_gtest.patch')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_INSTALL_LIBDIR:PATH={0}'.format(
                self.prefix.lib),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DSNAPPY_BUILD_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]

        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if '+pic' in self.spec:
            if name == 'cflags':
                flags.append(self.compiler.cc_pic_flag)
            elif name == 'cxxflags':
                flags.append(self.compiler.cxx_pic_flag)
        return (None, None, flags)

    @run_after('install')
    def install_pkgconfig(self):
        mkdirp(self.prefix.lib.pkgconfig)

        with open(join_path(self.prefix.lib.pkgconfig, 'snappy.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(self.prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(self.prefix.lib))
            f.write('includedir={0}\n'.format(self.prefix.include))
            f.write('\n')
            f.write('Name: Snappy\n')
            f.write('Description: A fast compressor/decompressor.\n')
            f.write('Version: {0}\n'.format(self.spec.version))
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -lsnappy\n')
