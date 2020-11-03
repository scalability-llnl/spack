# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Caliper(CMakePackage):
    """Caliper is a program instrumentation and performance measurement
    framework. It is designed as a performance analysis toolbox in a
    library, allowing one to bake performance analysis capabilities
    directly into applications and activate them at runtime.
    """

    homepage = "https://github.com/LLNL/Caliper"
    git      = "https://github.com/LLNL/Caliper.git"

    version('master')
    version('2.4.0', tag='v2.4.0')
    version('2.3.0', tag='v2.3.0')
    version('2.2.0', tag='v2.2.0')
    version('2.1.1', tag='v2.1.1')
    version('2.0.1', tag='v2.0.1')
    version('1.9.1', tag='v1.9.1')
    version('1.9.0', tag='v1.9.0')
    version('1.8.0', tag='v1.8.0')
    version('1.7.0', tag='v1.7.0')

    is_linux = sys.platform.startswith('linux')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('adiak', default=True,
            description='Enable Adiak support')
    variant('mpi', default=True,
            description='Enable MPI wrappers')
    variant('dyninst', default=False,
            description='Enable symbol translation support with dyninst')
    # libunwind has some issues on Mac
    variant('callpath', default=sys.platform != 'darwin',
            description='Enable callpath service (requires libunwind)')
    # pthread_self() signature is incompatible with PAPI_thread_init() on Mac
    variant('papi', default=sys.platform != 'darwin',
            description='Enable PAPI service')
    variant('libpfm', default=is_linux,
            description='Enable libpfm (perf_events) service')
    # Gotcha is Linux-only
    variant('gotcha', default=is_linux,
            description='Enable GOTCHA support')
    variant('sampler', default=is_linux,
            description='Enable sampling support on Linux')
    variant('sosflow', default=False,
            description='Enable SOSflow support')

    depends_on('adiak@0.1:0.99', when='@2.2: +adiak')

    depends_on('dyninst@10.0:10.99', when='@2: +dyninst')

    depends_on('papi@5.3:5.99', when='@:2.2 +papi')
    depends_on('papi@5.3:6.99', when='@2.3: +papi')

    depends_on('libpfm4@4.8:4.99', when='+libpfm')

    depends_on('mpi', when='+mpi')
    depends_on('unwind@1.2:1.99', when='+callpath')

    depends_on('sosflow@spack', when='@1.0:1.99+sosflow')

    depends_on('cmake',  type='build')
    depends_on('python', type='build')

    # sosflow support not yet in 2.0
    conflicts('+sosflow', '@2.0.0:2.4.99')
    conflicts('+adiak', '@:2.1.99')

    # The Dyninst 9.X used by v1.9.X is deprecated
    conflicts('+dyninst', when='@:1.99',
              msg='Dyninst unsupported by version <=2.0.1')

    patch('for_aarch64.patch', when='target=aarch64:')

    def cmake_args(self):
        spec = self.spec

        args = [
            ('-DPYTHON_EXECUTABLE=%s' %
                spec['python'].command.path),
            '-DBUILD_TESTING=Off',
            '-DBUILD_DOCS=Off',
            '-DBUILD_SHARED_LIBS=%s' % ('On' if '+shared'  in spec else 'Off'),
            '-DWITH_ADIAK=%s'    % ('On' if '+adiak'    in spec else 'Off'),
            '-DWITH_DYNINST=%s'  % ('On' if '+dyninst'  in spec else 'Off'),
            '-DWITH_CALLPATH=%s' % ('On' if '+callpath' in spec else 'Off'),
            '-DWITH_GOTCHA=%s'   % ('On' if '+gotcha'   in spec else 'Off'),
            '-DWITH_PAPI=%s'     % ('On' if '+papi'     in spec else 'Off'),
            '-DWITH_LIBPFM=%s'   % ('On' if '+libpfm'   in spec else 'Off'),
            '-DWITH_SOSFLOW=%s'  % ('On' if '+sosflow'  in spec else 'Off'),
            '-DWITH_SAMPLER=%s'  % ('On' if '+sampler'  in spec else 'Off'),
            '-DWITH_MPI=%s'      % ('On' if '+mpi'      in spec else 'Off')
        ]

        if '+papi' in spec:
            args.append('-DPAPI_PREFIX=%s'    % spec['papi'].prefix)
        if '+libpfm' in spec:
            args.append('-DLIBPFM_INSTALL=%s' % spec['libpfm4'].prefix)
        if '+sosflow' in spec:
            args.append('-DSOS_PREFIX=%s'     % spec['sosflow'].prefix)
        if '+callpath' in spec:
            args.append('-DLIBUNWIND_PREFIX=%s' % spec['libunwind'].prefix)

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx)

        return args
