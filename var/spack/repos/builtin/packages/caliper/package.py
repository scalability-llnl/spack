# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Caliper(CMakePackage, CudaPackage):
    """Caliper is a program instrumentation and performance measurement
    framework. It is designed as a performance analysis toolbox in a
    library, allowing one to bake performance analysis capabilities
    directly into applications and activate them at runtime.
    """

    homepage = "https://github.com/LLNL/Caliper"
    git      = "https://github.com/LLNL/Caliper.git"
    url      = "https://github.com/LLNL/Caliper/archive/v2.5.0.tar.gz"

    maintainers = ["daboehme"]

    version('master', branch='master')
    version('2.5.0', sha256='d553e60697d61c53de369b9ca464eb30710bda90fba9671201543b64eeac943c')
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
    # libunwind has some issues on Mac
    variant('libunwind', default=sys.platform != 'darwin',
            description='Enable stack unwind support')
    variant('libdw', default=is_linux,
            description='Enable DWARF symbol lookup')
    # pthread_self() signature is incompatible with PAPI_thread_init() on Mac
    variant('papi', default=sys.platform != 'darwin',
            description='Enable PAPI service')
    variant('libpfm', default=False,
            description='Enable libpfm (perf_events) service')
    # Gotcha is Linux-only
    variant('gotcha', default=is_linux,
            description='Enable GOTCHA support')
    variant('sampler', default=is_linux,
            description='Enable sampling support on Linux')
    variant('sosflow', default=False,
            description='Enable SOSflow support')
    variant('fortran', default=False,
            description='Enable Fortran support')

    depends_on('adiak@0.1:0.99', when='@2.2: +adiak')

    depends_on('papi@5.3:5.99', when='@:2.2 +papi')
    depends_on('papi@5.3:6.99', when='@2.3: +papi')

    depends_on('libpfm4@4.8:4.99', when='+libpfm')

    depends_on('mpi', when='+mpi')
    depends_on('unwind@1.2:1.99', when='+libunwind')
    depends_on('elfutils', when='+libdw')

    depends_on('sosflow@spack', when='@1.0:1.99+sosflow')

    depends_on('cmake',  type='build')
    depends_on('python', type='build')

    # sosflow support not yet in 2.0
    conflicts('+sosflow', '@2.0.0:2.5.99')
    conflicts('+adiak', '@:2.1.99')
    conflicts('+libdw', '@:2.4.99')

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
            '-DWITH_GOTCHA=%s'   % ('On' if '+gotcha'   in spec else 'Off'),
            '-DWITH_PAPI=%s'     % ('On' if '+papi'     in spec else 'Off'),
            '-DWITH_LIBDW=%s'    % ('On' if '+libdw'    in spec else 'Off'),
            '-DWITH_LIBPFM=%s'   % ('On' if '+libpfm'   in spec else 'Off'),
            '-DWITH_SOSFLOW=%s'  % ('On' if '+sosflow'  in spec else 'Off'),
            '-DWITH_SAMPLER=%s'  % ('On' if '+sampler'  in spec else 'Off'),
            '-DWITH_MPI=%s'      % ('On' if '+mpi'      in spec else 'Off'),
            '-DWITH_FORTRAN=%s'  % ('On' if '+fortran'  in spec else 'Off')
        ]

        if '+papi' in spec:
            args.append('-DPAPI_PREFIX=%s'    % spec['papi'].prefix)
        if '+libdw' in spec:
            args.append('-DLIBDW_PREFIX=%s'   % spec['elfutils'].prefix)
        if '+libpfm' in spec:
            args.append('-DLIBPFM_INSTALL=%s' % spec['libpfm4'].prefix)
        if '+sosflow' in spec:
            args.append('-DSOS_PREFIX=%s'     % spec['sosflow'].prefix)

        # -DWITH_CALLPATH was renamed -DWITH_LIBUNWIND in 2.5
        callpath_flag = 'LIBUNWIND' if spec.satisfies('@2.5:') else 'CALLPATH'
        if '+libunwind' in spec:
            args.append('-DLIBUNWIND_PREFIX=%s' % spec['unwind'].prefix)
            args.append('-DWITH_%s=On'  % callpath_flag)
        else:
            args.append('-DWITH_%s=Off' % callpath_flag)

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx)

        if '+cuda' in spec:
            args.append('-DCUDA_TOOLKIT_ROOT_DIR=%s' % spec['cuda'].prefix)
            # technically only works with cuda 10.2+, otherwise cupti is in
            # ${CUDA_TOOLKIT_ROOT_DIR}/extras/CUPTI
            args.append('-DCUPTI_PREFIX=%s' % spec['cuda'].prefix)
            args.append('-DWITH_NVTX=On')
            args.append('-DWITH_CUPTI=On')
        else:
            args.append('-DWITH_NVTX=Off')
            args.append('-DWITH_CUPTI=Off')

        return args
