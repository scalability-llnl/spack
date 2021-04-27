# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flatbuffers(CMakePackage):
    """Memory Efficient Serialization Library
    """

    homepage = "http://google.github.io/flatbuffers/"
    url      = "https://github.com/google/flatbuffers/archive/v1.9.0.tar.gz"

    version('1.12.0', sha256='62f2223fb9181d1d6338451375628975775f7522185266cd5296571ac152bc45')
    version('1.11.0', sha256='3f4a286642094f45b1b77228656fbd7ea123964f19502f9ecfd29933fd23a50b')
    version('1.10.0', sha256='3714e3db8c51e43028e10ad7adffb9a36fc4aa5b1a363c2d0c4303dd1be59a7c')
    version('1.9.0', sha256='5ca5491e4260cacae30f1a5786d109230db3f3a6e5a0eb45d0d0608293d247e3')
    version('1.8.0', sha256='c45029c0a0f1a88d416af143e34de96b3091642722aa2d8c090916c6d1498c2e')

    variant('shared', default=True,
            description='Build shared instead of static libraries')
    variant('python', default=False,
            description='Build with python support')

    depends_on('py-setuptools', when='+python', type='build')
    depends_on('python@3.6:', when='+python', type=('build', 'run'))
    extends('python', when='+python')

    # Fixes "Class-memaccess" compilation error in test
    # https://github.com/google/flatbuffers/issues/5930
    # Possibly affects earlier releases but I haven't tried to apply it.
    patch('https://raw.githubusercontent.com/Flamefire/easybuild-easyconfigs/'
          '72ba2a1a0d44fbd96ded9f279373ef804bdf3903/easybuild/easyconfigs/f/'
          'flatbuffers/flatbuffers-1.12.0_replace-usage-of-memset.patch',
          sha256='094a98b5a7debbc2c60c2b235942c79e505ec76f9281f87c95d15e9ad8a97c52',
          when='@1.12.0:%gcc@10:')
    # Silences false positive "-Wstringop-overflow" on GCC 10+
    # https://github.com/google/flatbuffers/issues/5950
    # Possibly affects earlier releases but I haven't tried to apply it.
    patch('https://patch-diff.githubusercontent.com/raw/google/flatbuffers/pull/'
          '6020.patch',
          sha256='4a9a18abc776407f3f97e02c40f349cfb24fe7ddb41df952271d894777a31c88',
          when='@1.12.0:%gcc@10:')

    @run_after('install')
    def python_install(self):
        if '+python' in self.spec:
            pydir = join_path(self.stage.source_path, 'python')
            with working_dir(pydir):
                setup_py('install', '--prefix=' + prefix,
                         '--single-version-externally-managed', '--root=/')

    def cmake_args(self):
        args = []
        args.append('-DFLATBUFFERS_BUILD_SHAREDLIB={0}'.format(
            'ON' if '+shared' in self.spec else 'OFF'))
        args.append('-DFLATBUFFERS_BUILD_FLATLIB={0}'.format(
            'ON' if '+shared' not in self.spec else 'OFF'))
        if 'darwin' in self.spec.architecture:
            args.append('-DCMAKE_MACOSX_RPATH=ON')
        return args
