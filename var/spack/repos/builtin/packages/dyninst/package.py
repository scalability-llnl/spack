# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost
import os.path


class Dyninst(CMakePackage):
    """API for dynamic binary instrumentation.  Modify programs while they
    are executing without recompiling, re-linking, or re-executing."""

    homepage = "https://dyninst.org"
    git      = "https://github.com/dyninst/dyninst.git"
    maintainers = ['hainest']

    version('master', branch='master')
    version('10.2.1', tag='v10.2.1')
    version('10.2.0', tag='v10.2.0')
    version('10.1.0', tag='v10.1.0')
    version('10.0.0', tag='v10.0.0')
    version('9.3.2', tag='v9.3.2')
    version('9.3.0', tag='v9.3.0')
    version('9.2.0', tag='v9.2.0')
    version('9.1.0', tag='v9.1.0')
    version('8.2.1', tag='v8.2.1')

    variant('openmp', default=True,
            description='Enable OpenMP support for ParseAPI '
            '(version 10.0.0 or later)')

    variant('static', default=False,
            description='Build static libraries')

    variant('stat_dysect', default=False,
            description="Patch for STAT's DySectAPI")

    boost_libs = '+atomic+chrono+date_time+filesystem+system+thread+timer'

    depends_on('boost@1.61.0:' + boost_libs, when='@10.1.0:')
    depends_on('boost@1.61.0:1.69.99' + boost_libs, when='@:10.0.99')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('libiberty+pic')

    # Dyninst uses elfutils starting with 9.3.0, and used libelf
    # before that.
    depends_on('elfutils', type='link', when='@9.3.0:')
    depends_on('libelf', type='link', when='@:9.2.99')

    # Dyninst uses libdw from elfutils starting with 10.0, and used
    # libdwarf before that.
    depends_on('libdwarf', when='@:9.99.99')

    depends_on('tbb@2018.6:', when='@10.0.0:')

    depends_on('cmake@3.4.0:', type='build', when='@10.1.0:')
    depends_on('cmake@3.0.0:', type='build', when='@10.0.0:10.0.99')
    depends_on('cmake@2.8:', type='build', when='@:9.99.99')

    patch('stat_dysect.patch', when='+stat_dysect')
    patch('stackanalysis_h.patch', when='@9.2.0')
    patch('v9.3.2-auto.patch', when='@9.3.2 %gcc@:4.7.99')
    patch('tribool.patch', when='@9.3.0:10.0.0 ^boost@1.69:')

    # No Mac support (including apple-clang)
    conflicts('platform=darwin', msg='macOS is not supported')

    # We currently only build with gcc
    conflicts('%clang')
    conflicts('%arm')
    conflicts('%cce')
    conflicts('%fj')
    conflicts('%intel')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    # Versions 9.3.x used cotire, but have no knob to turn it off.
    # Cotire has no real use for one-time builds and can break
    # parallel builds with both static and shared libs.
    @when('@9.3.0:9.3.99')
    def patch(self):
        filter_file('USE_COTIRE true', 'USE_COTIRE false',
                    'cmake/shared.cmake')

    # New style cmake args, starting with 10.1.
    @when('@10.1.0:')
    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBoost_ROOT_DIR=%s'     % spec['boost'].prefix,
            '-DElfUtils_ROOT_DIR=%s'  % spec['elf'].prefix,
            '-DLibIberty_ROOT_DIR=%s' % spec['libiberty'].prefix,
            '-DTBB_ROOT_DIR=%s'       % spec['tbb'].prefix,
        ]

        if '+openmp' in spec:
            args.append('-DUSE_OpenMP=ON')
        else:
            args.append('-DUSE_OpenMP=OFF')

        if '+static' in spec:
            args.append('-DENABLE_STATIC_LIBS=YES')
        else:
            args.append('-DENABLE_STATIC_LIBS=NO')

        # Make sure Dyninst doesn't try to build its own dependencies
        # outside of Spack
        if spec.satisfies('@10.2.0:'):
            args.append('-DSTERILE_BUILD=ON')

        return args

    # Old style cmake args, up through 10.0.
    @when('@:10.0.99')
    def cmake_args(self):
        spec = self.spec

        # Elf -- the directory containing libelf.h.
        elf = spec['elf'].prefix
        elf_include = os.path.dirname(
            find_headers('libelf', elf.include, recursive=True)[0])

        # Dwarf -- the directory containing elfutils/libdw.h or
        # libdwarf.h, and the path to libdw.so or libdwarf.so.
        if spec.satisfies('@10.0.0:'):
            dwarf_include = elf.include
            dwarf_lib = find_libraries('libdw', elf, recursive=True)
        else:
            dwarf_include = spec['libdwarf'].prefix.include
            dwarf_lib = spec['libdwarf'].libs

        args = [
            '-DPATH_BOOST=%s' % spec['boost'].prefix,
            '-DIBERTY_LIBRARIES=%s' % spec['libiberty'].libs,

            '-DLIBELF_INCLUDE_DIR=%s' % elf_include,
            '-DLIBELF_LIBRARIES=%s' % spec['elf'].libs,

            '-DLIBDWARF_INCLUDE_DIR=%s' % dwarf_include,
            '-DLIBDWARF_LIBRARIES=%s' % dwarf_lib,
        ]

        # TBB include and lib directories, version 10.x or later.
        if spec.satisfies('@10.0.0:'):
            args.extend([
                '-DTBB_INCLUDE_DIRS=%s' % spec['tbb'].prefix.include,
                '-DTBB_LIBRARY=%s' % spec['tbb'].prefix.lib,
            ])

        # Openmp applies to version 10.x or later.
        if spec.satisfies('@10.0.0:'):
            if '+openmp' in spec:
                args.append('-DUSE_OpenMP=ON')
            else:
                args.append('-DUSE_OpenMP=OFF')

        # Static libs started with version 9.1.0.
        if spec.satisfies('@9.1.0:'):
            if '+static' in spec:
                args.append('-DENABLE_STATIC_LIBS=1')
            else:
                args.append('-DENABLE_STATIC_LIBS=NO')

        return args
