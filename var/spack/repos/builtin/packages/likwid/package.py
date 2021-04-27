# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Likwid(Package):
    """Likwid is a simple to install and use toolsuite of command line
    applications for performance oriented programmers. It works for Intel and
    AMD processors on the Linux operating system. This version uses the
    perf_event backend which reduces the feature set but allows user installs.
    See https://github.com/RRZE-HPC/likwid/wiki/TutorialLikwidPerf#feature-limitations
    for information."""

    homepage = "https://hpc.fau.de/research/tools/likwid/"
    url      = "https://github.com/RRZE-HPC/likwid/archive/v5.0.0.tar.gz"
    git      = "https://github.com/RRZE-HPC/likwid.git"
    maintainers = ['TomTheBear']

    version('5.1.1', sha256='faec7c62987967232f476a6ff0ee85af686fd24b5a360126896b7f435d1f943f')
    version('5.1.0', sha256='5a180702a1656c6315b861a85031ab4cb090424aec42cbbb326b849e29f55571')
    version('5.0.2', sha256='0a1c8984e4b43ea8b99d09456ef05035eb934594af1669432117585c638a2da4')
    version('5.0.1', sha256='3757b0cb66e8af0116f9288c7f90543acbd8e2af8f72f77aef447ca2b3e76453')
    version('5.0.0', sha256='26623f5a1a5fec19d798f0114774a5293d1c93a148538b9591a13e50930fa41e')
    version('4.3.4', sha256='5c0d1c66b25dac8292a02232f06454067f031a238f010c62f40ef913c6609a83')
    version('4.3.3', sha256='a681378cd66c1679ca840fb5fac3136bfec93c01b3d78cc1d00a641db325a9a3')
    version('4.3.2', sha256='fd39529854b8952e7530da1684835aa43ac6ce2169f5ebd1fb2a481f6fb288ac')
    version('4.3.1', sha256='4b40a96717da54514274d166f9b71928545468091c939c1d74109733279eaeb1')
    version('4.3.0', sha256='86fc5f82c80fcff1a643394627839ec79f1ca2bcfad30000eb7018da592588b4')

    patch('https://github.com/RRZE-HPC/likwid/commit/e0332ace8fe8ca7dcd4b4477a25e37944f173a5c.patch', sha256='c3b8f939a46b425665577ce764d4fba080a23cab5999c53db71655fd54d7e0b1', when='@5.0.1')
    patch('https://github.com/RRZE-HPC/likwid/commit/d2d0ef333b5e0997d7c80fc6ac1a473b5e47d084.patch', sha256='636cbf40669261fdb36379d67253be2b731cfa7b6d610d232767d72fbdf08bc0', when='@4.3.4')
    patch('https://github.com/RRZE-HPC/likwid/files/5341379/likwid-lua5.1.patch.txt', sha256='bc56253c1e3436b5ba7bf4c5533d0391206900c8663c008f771a16376975e416', when='@5.0.2^lua@5.1')
    variant('fortran', default=True, description='with fortran interface')
    variant('cuda', default=False, description='with Nvidia GPU profiling support')

    # NOTE: There is no way to use an externally provided hwloc with Likwid.
    # The reason is that the internal hwloc is patched to contain extra
    # functionality and functions are prefixed with "likwid_".
    # Note: extra functionality was included in upstream hwloc

    depends_on('lua', when='@:4')
    depends_on('lua@5.2:', when='@5:5.0.1')
    depends_on('lua', when='@5.0.2:')
    depends_on('cuda', when='@5: +cuda')

    # TODO: check
    # depends_on('gnuplot', type='run')

    depends_on('perl', type=('build', 'run'))

    def patch(self):
        files = glob.glob('perl/*.*') + glob.glob('bench/perl/*.*')

        # Allow the scripts to find Spack's perl
        filter_file('^#!/usr/bin/perl -w', '#!/usr/bin/env perl', *files)
        filter_file('^#!/usr/bin/perl', '#!/usr/bin/env perl', *files)

    def setup_run_environment(self, env):
        if "+cuda" in self.spec:
            libs = find_libraries('libcupti', root=self.spec['cuda'].prefix,
                                  shared=True, recursive=True)
            for lib in libs.directories:
                env.append_path('LD_LIBRARY_PATH', lib)

    @run_before('install')
    def filter_sbang(self):
        # Filter sbang before install so Spack's sbang hook can fix it up
        files = ['perl/feedGnuplot'] + glob.glob('filters/*')

        filter_file('^#!/usr/bin/perl',
                    '#!{0}'.format(self.spec['perl'].command.path),
                    *files)

    def install(self, spec, prefix):
        supported_compilers = {
            'apple-clang': 'CLANG',
            'clang': 'CLANG',
            'gcc': 'GCC',
            'intel': 'ICC'
        }
        if spec.target.family == 'aarch64':
            supported_compilers = {
                'gcc': 'GCCARMv8', 'clang': 'ARMCLANG', 'arm': 'ARMCLANG'}
        elif spec.target.family == 'ppc64' or spec.target.family == 'ppc64le':
            supported_compilers = {'gcc': 'GCCPOWER'}
        if self.compiler.name not in supported_compilers:
            raise RuntimeError('{0} is not a supported compiler \
            to compile Likwid'.format(self.compiler.name))

        filter_file('^COMPILER .*',
                    'COMPILER = ' +
                    supported_compilers[self.compiler.name],
                    'config.mk')
        filter_file('^PREFIX .*',
                    'PREFIX = ' +
                    prefix,
                    'config.mk')

        # FIXME: once https://github.com/spack/spack/issues/4432 is
        # resolved, install as root by default and remove this
        filter_file('^ACCESSMODE .*',
                    'ACCESSMODE = perf_event',
                    'config.mk')
        filter_file('^BUILDFREQ .*',
                    'BUILDFREQ = false',
                    'config.mk')
        filter_file('^BUILDDAEMON .*',
                    'BUILDDAEMON = false',
                    'config.mk')

        if '+fortran' in self.spec:
            filter_file('^FORTRAN_INTERFACE .*',
                        'FORTRAN_INTERFACE = true',
                        'config.mk')
            if self.compiler.name == 'gcc':
                makepath = join_path('make', 'include_GCC.mk')
                filter_file('ifort', 'gfortran', makepath)
                filter_file('-module', '-I',  makepath)
        else:
            filter_file('^FORTRAN_INTERFACE .*',
                        'FORTRAN_INTERFACE = false',
                        'config.mk')

        if "+cuda" in self.spec:
            filter_file('^NVIDIA_INTERFACE.*',
                        'NVIDIA_INTERFACE = true',
                        'config.mk')
            filter_file('^BUILDAPPDAEMON.*',
                        'BUILDAPPDAEMON = true',
                        'config.mk')
            cudainc = spec['cuda'].prefix.include
            filter_file('^CUDAINCLUDE.*',
                        'CUDAINCLUDE = {0}'.format(cudainc),
                        'config.mk')
            cuptihead = HeaderList(find(spec['cuda'].prefix, 'cupti.h',
                                        recursive=True))
            filter_file('^CUPTIINCLUDE.*',
                        'CUPTIINCLUDE = {0}'.format(cuptihead.directories[0]),
                        'config.mk')
        else:
            filter_file('^NVIDIA_INTERFACE.*',
                        'NVIDIA_INTERFACE = false',
                        'config.mk')

        if spec.satisfies('^lua'):
            filter_file('^#LUA_INCLUDE_DIR.*',
                        'LUA_INCLUDE_DIR = {0}'.format(
                            spec['lua'].prefix.include),
                        'config.mk')
            filter_file('^#LUA_LIB_DIR.*',
                        'LUA_LIB_DIR = {0}'.format(
                            spec['lua'].prefix.lib),
                        'config.mk')
            filter_file('^#LUA_LIB_NAME.*',
                        'LUA_LIB_NAME = lua',
                        'config.mk')
            filter_file('^#LUA_BIN.*',
                        'LUA_BIN = {0}'.format(
                            spec['lua'].prefix.bin),
                        'config.mk')

        # https://github.com/RRZE-HPC/likwid/issues/287
        if self.spec.satisfies('@:5.0.2 %gcc@10:'):
            filter_file(r'^(CFLAGS.*)',
                        '\\1 -fcommon',
                        'make/include_GCC.mk')

        env['PWD'] = os.getcwd()
        make()
        make('install')
