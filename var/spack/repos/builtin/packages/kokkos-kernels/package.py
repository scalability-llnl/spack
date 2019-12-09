# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosKernels(Package):
    """Kokkos C++ Performance Portability Programming EcoSystem: Math Kernels -
    Provides BLAS, Sparse BLAS and Graph Kernels."""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    url      = "https://github.com/kokkos/kokkos-kernels/archive/2.7.00.tar.gz"
    git      = "https://github.com/kokkos/kokkos-kernels.git"

    version('develop', branch='develop')
    version('2.9.00', sha256='dafa9ebcdbcdc95641a986a80fcd3e532f1d80692c80a51cb08182c02c1added')
    version('2.8.00', sha256='c9648dbf5b9cbddf2aa72f6d214a2c40e23e51660f903b83743617251574fe06')
    version('2.7.00', sha256='adf4af44eadbdfbeb9ec69dd5fae4e2852bd1fbe4a69213efd199e49f4098254')
    version('2.5.00', sha256='2c2289da3a41dafd97726e90507debafbb9f5e49ca5b0f5c8d1e044a5796f000')

    variant('debug', default=False, description="Build debug version of Kokkos")

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('pthreads', default=False, description="enable Pthreads backend")
    variant('qthreads', default=False, description="enable Qthreads backend")
    variant('cuda', default=False, description="enable Cuda backend")
    variant('openmp', default=False, description="enable OpenMP backend")

    # Compilation options
    variant('pic', default=False,
            description="enable position independent code (-fPIC flag)")

    # Kokkos options
    variant('aggressive_vectorization', default=False,
            description="set aggressive_vectorization Kokkos option")
    variant('disable_profiling', default=False,
            description="set disable_profiling Kokkos option")
    variant('disable_dualview_modify_check', default=False,
            description="set disable_dualview_modify_check Kokkos option")
    variant('enable_profile_load_print', default=False,
            description="set enable_profile_load_print Kokkos option")
    variant('compiler_warnings', default=False,
            description="set compiler_warnings Kokkos option")
    variant('disable_deprecated_code', default=False,
            description="set disable_deprecated_code Kokkos option")
    variant('enable_eti', default=False,
            description="set enable_eti Kokkos option")

    # CUDA options
    variant('force_uvm', default=False,
            description="set force_uvm Kokkos CUDA option")
    variant('use_ldg', default=False,
            description="set use_ldg Kokkos CUDA option")
    variant('rdc', default=False,
            description="set rdc Kokkos CUDA option")
    variant('enable_lambda', default=False,
            description="set enable_lambda Kokkos CUDA option")

    host_values = ('AMDAVX', 'ARMv80', 'ARMv81', 'ARMv8-ThunderX',
                   'Power7', 'Power8', 'Power9',
                   'WSM', 'SNB', 'HSW', 'BDW', 'SKX',
                   'KNC', 'KNL')

    gpu_values = ('Kepler30', 'Kepler32', 'Kepler35', 'Kepler37',
                  'Maxwell50', 'Maxwell52', 'Maxwell53',
                  'Pascal60', 'Pascal61',
                  'Volta70', 'Volta72')

    # C++ standard variant
    variant('cxxstd', default='none',
            values=('c++11', 'c++14', 'c++17', 'c++1y', 'c++1z', 'c++2a'),
            multi=False,
            description='set cxxstandard Kokkos option')

    # Host architecture variant
    variant(
        'host_arch',
        default='none',
        values=host_values,
        description='Set the host architecture to use'
    )

    # GPU architecture variant
    variant(
        'gpu_arch',
        default='none',
        values=gpu_values,
        description='Set the GPU architecture to use'
    )

    # Checks on Kokkos version and Kokkos options
    conflicts('+aggressive_vectorization', when='@:2.0.99',)
    conflicts('+disable_profiling', when='@:2.0.99',)
    conflicts('+disable_dualview_modify_check', when='@:2.03.04',)
    conflicts('+enable_profile_load_print', when='@:2.03.04',)
    conflicts('+compiler_warnings', when='@:2.03.14',)
    conflicts('+disable_deprecated_code', when='@:2.5.99',)
    conflicts('+enable_eti', when='@:2.6.99',)

    # Check that we haven't specified a gpu architecture
    # without specifying CUDA
    for p in gpu_values:
        conflicts('gpu_arch={0}'.format(p), when='~cuda',
                  msg='Must specify CUDA backend to use a GPU architecture.')

    # Check that we haven't specified a Kokkos CUDA option
    # without specifying CUDA
    conflicts('+force_uvm', when='~cuda',
              msg='Must enable CUDA to use force_uvm.')
    conflicts('+use_ldg', when='~cuda',
              msg='Must enable CUDA to use use_ldg.')
    conflicts('+rdc', when='~cuda',
              msg='Must enable CUDA to use rdc.')
    conflicts('+enable_lambda', when='~cuda',
              msg='Must enable CUDA to use enable_lambda.')

    # Check that we haven't asked for a GPU architecture that
    # the revision of kokkos does not support
    conflicts('gpu_arch=Volta70', when='@:2.5.99')
    conflicts('gpu_arch=Volta72', when='@:2.5.99')

    # conflicts on kokkos version and cuda enabled
    # see kokkos issue #1296
    # https://github.com/kokkos/kokkos/issues/1296
    conflicts('+cuda', when='@2.5.00:2.7.00',
              msg='Kokkos build system has issue (#1296) when CUDA enabled'
              ' in version 2.5.00 through 2.7.00.')

    # Resources
    # 
    resource(
        name='kokkos-base',
        sha256='e0621197791ed3a381b4f02c78fa529f3cff3abb74d52157b4add17e8aa04bc4',
        url='https://github.com/kokkos/kokkos/archive/2.9.00.tar.gz',
        placement='kokkos-base',
        when='@2.9.0',
    )
    resource(
        name='kokkos-base',
        sha256='1c72661f2d770517bff98837001b42b9c677d1df29f7493a1d7c008549aff630',
        url='https://github.com/kokkos/kokkos/archive/2.8.00.tar.gz',
        placement='kokkos-base',
        when='@2.8.0',
    )
    resource(
        name='kokkos-base',
        sha256='01595996e612ef7410aa42fa265a23101cfe1b6993fa9810ca844db5c89ad765',
        url='https://github.com/kokkos/kokkos/archive/2.7.00.tar.gz',
        placement='kokkos-base',
        when='@2.7.0',
    )
    resource(
        name='kokkos-base',
        sha256='ea232594bf746abb99ae2aafaeef5d07adc089968010a62a88aaa892106d9476',
        url='https://github.com/kokkos/kokkos/archive/2.5.00.tar.gz',
        placement='kokkos-base',
        when='@2.5.0',
    )

    # Specify that v1.x is required as v2.x has API changes
    depends_on('hwloc@:1')
    depends_on('qthreads', when='+qthreads')
    depends_on('cuda', when='+cuda')


    # check wiki for more options
    def install(self, spec, prefix):
        generate = which(join_path(self.stage.source_path,
                                   'scripts/generate_makefile.bash'))
        with working_dir('build', create=True):
            g_args = [
                '--prefix=%s' % prefix,
                '--with-hwloc=%s' % spec['hwloc'].prefix,
                '--kokkos-path=%s' % join_path(self.stage.source_path, 'kokkos-base'),
                '--kokkoskernels-path=%s' % self.stage.source_path,
                # This reduces compile times significantly
                #
                '--with-scalars="float,double"',
                '--with-ordinals=""',
                '--with-offsets=""',
                '--with-layouts=""'
            ]
            arch_args = []
            kokkos_kernels_options_args = ['blas-mangle_']
            kokkos_options_args = []
            cuda_options_args = []

            # PIC
            if '+pic' in spec:
                g_args.append('--cxxflags=-fPIC')

            # C++ standard
            cxxstandard = spec.variants['cxxstd'].value
            if cxxstandard != 'none':
                g_args.append('--cxxstandard=%s' % cxxstandard)

            # Build Debug
            if '+debug' in spec:
                g_args.append('--debug')

            # Backends
            if '+serial' in spec:
                g_args.append('--with-serial')
            if '+openmp' in spec:
                g_args.append('--with-openmp')
            if '+pthreads' in spec:
                g_args.append('--with-pthread')
            if '+qthreads' in spec:
                g_args.append('--with-qthreads=%s' % spec['qthreads'].prefix)
            if '+cuda' in spec:
                g_args.append('--with-cuda=%s' % spec['cuda'].prefix)
            # Host architectures
            host_arch = spec.variants['host_arch'].value
            # GPU architectures
            gpu_arch  = spec.variants['gpu_arch'].value
            if host_arch != 'none':
                arch_args.append(host_arch)
            if gpu_arch != 'none':
                arch_args.append(gpu_arch)
            # Combined architecture flags
            if arch_args:
                g_args.append('--arch={0}'.format(','.join(arch_args)))

            # CUDA options
            if '+force_uvm' in spec:
                cuda_options_args.append('force_uvm')
            if '+use_ldg' in spec:
                cuda_options_args.append('use_ldg')
            if '+rdc' in spec:
                cuda_options_args.append('rdc')
            if '+enable_lambda' in spec:
                cuda_options_args.append('enable_lambda')
            if cuda_options_args:
                g_args.append('--with-cuda-options={0}'
                              .format(','.join(cuda_options_args)))

            # Kokkos-kernels options
            #if '+enable_eti' in spec:
            #    kokkos_kernels_options_args.append('enable_eti')
            #g_args.append('--with-options={0}'
            #              .format(','.join(kokkos_kernels_options_args)))

            # Kokkos options
            if '+aggressive_vectorization' in spec:
                kokkos_options_args.append('aggressive_vectorization')
            if '+disable_profiling' in spec:
                kokkos_options_args.append('disable_profiling')
            if '+disable_dualview_modify_check' in spec:
                kokkos_options_args.append('disable_dualview_modify_check')
            if '+enable_profile_load_print' in spec:
                kokkos_options_args.append('enable_profile_load_print')
            if '+compiler_warnings' in spec:
                kokkos_options_args.append('compiler_warnings')
            if '+disable_deprecated_code' in spec:
                kokkos_options_args.append('disable_deprecated_code')
            if '+enable_eti' in spec:
                kokkos_options_args.append('enable_eti')
            if kokkos_options_args:
                g_args.append('--with-kokkos-options={0}'
                              .format(','.join(kokkos_options_args)))

            generate(*g_args)
            make()
            make('install-lib')
