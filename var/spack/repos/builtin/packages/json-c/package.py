# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JsonC(CMakePackage):
    """A JSON implementation in C."""
    homepage = "https://github.com/json-c/json-c/wiki"
    url      = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.15.tar.gz"

    version('0.15', sha256='b8d80a1ddb718b3ba7492916237bbf86609e9709fb007e7f7d4322f02341a4c6')
    version('0.14', sha256='b377de08c9b23ca3b37d9a9828107dff1de5ce208ff4ebb35005a794f30c6870')
    version('0.13.1', sha256='b87e608d4d3f7bfdd36ef78d56d53c74e66ab278d318b71e6002a369d36f4873')
    version('0.12.1', sha256='2a136451a7932d80b7d197b10441e26e39428d67b1443ec43bbba824705e1123')
    version('0.12',   sha256='000c01b2b3f82dcb4261751eb71f1b084404fb7d6a282f06074d3c17078b9f3f')
    version('0.11',   sha256='28dfc65145dc0d4df1dfe7701ac173c4e5f9347176c8983edbfac9149494448c')

    depends_on('autoconf', when='@:0.13.1', type='build')

    parallel = False

    @when('@0.12:0.12.1 %gcc@7:')
    def patch(self):
        filter_file('-Wextra',
                    '-Wextra -Wno-error=implicit-fallthrough '
                    '-Wno-error=unused-but-set-variable',
                    'Makefile.in')

    @when('@:0.13.1')
    def cmake(self, spec, prefix):
        configure_args = ['--prefix=' + prefix]
        configure(*configure_args)

    @when('@:0.13.1')
    def build(self, spec, prefix):
        make()

    @when('@:0.13.1')
    def install(self, spec, prefix):
        make('install')

    @when('%cce@11.0.3:')
    def patch(self):
        filter_file('-Werror',
                    '',
                    'CMakeLists.txt')
