# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Superlu(Package):
    """SuperLU is a general purpose library for the direct solution of large,
    sparse, nonsymmetric systems of linear equations on high performance
    machines. SuperLU is designed for sequential machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/#superlu"
    url      = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_5.2.1.tar.gz"

    version('5.2.1', sha256='28fb66d6107ee66248d5cf508c79de03d0621852a0ddeba7301801d3d859f463')
    version('4.3', sha256='169920322eb9b9c6a334674231479d04df72440257c17870aaa0139d74416781')

    variant('pic',    default=True,
            description='Build with position independent code')

    depends_on('tcsh', type='build')
    depends_on('cmake', when='@5.2.1:', type='build')
    depends_on('blas')

    # CMake installation method
    def install(self, spec, prefix):
        cmake_args = [
            '-Denable_blaslib=OFF',
            '-DBLAS_blas_LIBRARY={0}'.format(spec['blas'].libs.joined())
        ]

        if '+pic' in spec:
            cmake_args.extend([
                '-DCMAKE_POSITION_INDEPENDENT_CODE=ON'
            ])

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

    # Pre-cmake installation method
    @when('@4.3')
    def install(self, spec, prefix):
        config = []

        # Define make.inc file
        config.extend([
            'PLAT       = _x86_64',
            'SuperLUroot = %s' % self.stage.source_path,
            # 'SUPERLULIB = $(SuperLUroot)/lib/libsuperlu$(PLAT).a',
            'SUPERLULIB = $(SuperLUroot)/lib/libsuperlu_{0}.a' \
            .format(self.spec.version),
            'BLASDEF    = -DUSE_VENDOR_BLAS',
            'BLASLIB    = {0}'.format(spec['blas'].libs.ld_flags),
            # or BLASLIB      = -L/usr/lib64 -lblas
            'TMGLIB     = libtmglib.a',
            'LIBS       = $(SUPERLULIB) $(BLASLIB)',
            'ARCH       = ar',
            'ARCHFLAGS  = cr',
            'RANLIB     = {0}'.format('ranlib' if which('ranlib') else 'echo'),
            'CC         = {0}'.format(env['CC']),
            'FORTRAN    = {0}'.format(env['FC']),
            'LOADER     = {0}'.format(env['CC']),
            'CDEFS      = -DAdd_'
        ])

        if '+pic' in spec:
            config.extend([
                # Use these lines instead when pic_flag capability arrives
                'CFLAGS     = -O3 {0}'.format(self.compiler.cc_pic_flag),
                'NOOPTS     = {0}'.format(self.compiler.cc_pic_flag),
                'FFLAGS     = -O2 {0}'.format(self.compiler.f77_pic_flag),
                'LOADOPTS   = {0}'.format(self.compiler.cc_pic_flag)
            ])
        else:
            config.extend([
                'CFLAGS     = -O3',
                'NOOPTS     = ',
                'FFLAGS     = -O2',
                'LOADOPTS   = '
            ])

        # Write configuration options to make.inc file
        with open('make.inc', 'w') as inc:
            for option in config:
                inc.write('{0}\n'.format(option))

        make(parallel=False)

        # Install manually
        install_tree('lib', prefix.lib)
        mkdir(prefix.include)
        install(join_path('SRC', '*.h'), prefix.include)
