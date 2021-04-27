# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Lz4(MakefilePackage):
    """LZ4 is lossless compression algorithm, providing compression speed
    at 400 MB/s per core, scalable with multi-cores CPU. It also features
    an extremely fast decoder, with speed in multiple GB/s per core,
    typically reaching RAM speed limits on multi-core systems."""

    homepage = "http://lz4.github.io/lz4/"
    url      = "https://github.com/lz4/lz4/archive/v1.9.2.tar.gz"

    version('1.9.3',   sha256='030644df4611007ff7dc962d981f390361e6c97a34e5cbc393ddfbe019ffe2c1')
    version('1.9.2',   sha256='658ba6191fa44c92280d4aa2c271b0f4fbc0e34d249578dd05e50e76d0e5efcc')
    version('1.9.0',   sha256='f8b6d5662fa534bd61227d313535721ae41a68c9d84058b7b7d86e143572dcfb')
    version('1.8.3',   sha256='33af5936ac06536805f9745e0b6d61da606a1f8b4cc5c04dd3cbaca3b9b4fc43')
    version('1.8.1.2', sha256='12f3a9e776a923275b2dc78ae138b4967ad6280863b77ff733028ce89b8123f9')
    version('1.7.5',   sha256='0190cacd63022ccb86f44fa5041dc6c3804407ad61550ca21c382827319e7e7e')
    version('1.3.1',   sha256='9d4d00614d6b9dec3114b33d1224b6262b99ace24434c53487a0c8fd0b18cfed')

    depends_on('valgrind', type='test')

    def url_for_version(self, version):
        url = "https://github.com/lz4/lz4/archive"

        if version > Version('1.3.1'):
            return "{0}/v{1}.tar.gz".format(url, version)
        else:
            return "{0}/r{1}.tar.gz".format(url, version.joined)

    def build(self, spec, prefix):
        par = True
        if spec.compiler.name == 'nvhpc':
            # relocation error when building shared and dynamic libs in
            # parallel
            par = False

        if sys.platform != "darwin":
            make('MOREFLAGS=-lrt', parallel=par)  # fixes make error on CentOS6
        else:
            make(parallel=par)

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc@:20.11'):
            filter_file('-fvisibility=hidden', '', 'Makefile')
            filter_file('-fvisibility=hidden', '', 'lib/Makefile')
            filter_file('-pedantic', '', 'Makefile')

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
