# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Magma(CMakePackage, CudaPackage):
    """The MAGMA project aims to develop a dense linear algebra library similar
       to LAPACK but for heterogeneous/hybrid architectures, starting with
       current "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"
    maintainers = ['stomov', 'luszczek']

    test_requires_compiler = True

    version('2.5.4', sha256='7734fb417ae0c367b418dea15096aef2e278a423e527c615aab47f0683683b67')
    version('2.5.3', sha256='c602d269a9f9a3df28f6a4f593be819abb12ed3fa413bba1ff8183de721c5ef6')
    version('2.5.2', sha256='065feb85558f9dd6f4cc4db36ac633a3f787827fc832d0b578a049a43a195620')
    version('2.5.1', sha256='ce32c199131515336b30c92a907effe0c441ebc5c5bdb255e4b06b2508de109f')
    version('2.5.0', sha256='4fd45c7e46bd9d9124253e7838bbfb9e6003c64c2c67ffcff02e6c36d2bcfa33')
    version('2.4.0', sha256='4eb839b1295405fd29c8a6f5b4ed578476010bf976af46573f80d1169f1f9a4f')
    version('2.3.0', sha256='010a4a057d7aa1e57b9426bffc0958f3d06913c9151463737e289e67dd9ea608')
    version('2.2.0', sha256='df5d4ace417e5bf52694eae0d91490c6bde4cde1b0da98e8d400c5c3a70d83a2')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')
    variant('shared', default=True,
            description='Enable shared library')
    variant('cuda', default=True, description='Build with CUDA')
    variant('cuda_arch', default='none', multi=True,
            description='Specify CUDA architecture(s)')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cuda@8:', when='@2.5.1:')  # See PR #14471

    conflicts('~cuda', msg='Magma requires cuda')
    conflicts('cuda_arch=none',
              msg='Please indicate a CUDA arch value or values')

    # currently not compatible with CUDA-11
    # https://bitbucket.org/icl/magma/issues/22/cuda-11-changes-issue
    # https://bitbucket.org/icl/magma/issues/25/error-cusparsesolveanalysisinfo_t-does-not
    conflicts('^cuda@11:', when='@:2.5.3')

    patch('ibm-xl.patch', when='@2.2:2.5.0%xl')
    patch('ibm-xl.patch', when='@2.2:2.5.0%xl_r')
    patch('magma-2.3.0-gcc-4.8.patch', when='@2.3.0%gcc@:4.8')
    patch('magma-2.5.0.patch', when='@2.5.0')
    patch('magma-2.5.0-cmake.patch', when='@2.5.0')
    patch('cmake-W.patch', when='@2.5.0:%nvhpc')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCMAKE_INSTALL_PREFIX=%s' % self.prefix,
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % self.prefix,
            '-DBLAS_LIBRARIES=%s' % spec['blas'].libs.joined(';'),
            # As of MAGMA v2.3.0, CMakeLists.txt does not use the variable
            # BLAS_LIBRARIES, but only LAPACK_LIBRARIES, so we need to
            # explicitly add blas to LAPACK_LIBRARIES.
            '-DLAPACK_LIBRARIES=%s' %
            (spec['lapack'].libs + spec['blas'].libs).joined(';')
        ])

        options += ['-DBUILD_SHARED_LIBS=%s' %
                    ('ON' if ('+shared' in spec) else 'OFF')]

        if '+fortran' in spec:
            options.extend([
                '-DUSE_FORTRAN=yes'
            ])
            if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
                options.extend([
                    '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77
                ])

        if spec.satisfies('^cuda'):
            cuda_arch = self.spec.variants['cuda_arch'].value
            if '@:2.2.0' in spec:
                capabilities = ' '.join('sm{0}'.format(i) for i in cuda_arch)
                options.extend(['-DGPU_TARGET=' + capabilities])
            else:
                capabilities = ' '.join('sm_{0}'.format(i) for i in cuda_arch)
                options.extend(['-DGPU_TARGET=' + capabilities])

        if '@2.5.0' in spec:
            options.extend(['-DMAGMA_SPARSE=OFF'])
            if spec.compiler.name in ['xl', 'xl_r']:
                options.extend(['-DCMAKE_DISABLE_FIND_PACKAGE_OpenMP=TRUE'])

        return options

    @run_after('install')
    def post_install(self):
        install('magmablas/atomics.cuh', self.prefix.include)
        install('control/magma_threadsetting.h', self.prefix.include)
        install('control/pthread_barrier.h', self.prefix.include)
        install('control/magma_internal.h', self.prefix.include)

    test_src_dir = 'example'

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.test_src_dir])

    def test(self):
        test_dir = join_path(self.install_test_root, self.test_src_dir)
        with working_dir(test_dir, create=False):
            magma_dir = 'MAGMADIR={0}'.format(self.prefix)
            cuda_dir = 'CUDADIR={0}'.format(self.spec['cuda'].prefix)
            blas_dir = 'OPENBLASDIR={0}'.format(self.spec['blas'].prefix)
            make(magma_dir, cuda_dir, blas_dir, 'c')
            self.run_test('./example_sparse',
                          purpose='MAGMA smoke test - sparse solver')
            self.run_test('./example_sparse_operator',
                          purpose='MAGMA smoke test - sparse operator')
            self.run_test('./example_v1',
                          purpose='MAGMA smoke test - legacy v1 interface')
            self.run_test('./example_v2',
                          purpose='MAGMA smoke test - v2 interface')
            if '+fortran' in self.spec:
                make(magma_dir, cuda_dir, blas_dir, 'fortran')
                self.run_test('./example_f',
                              purpose='MAGMA smoke test - Fortran interface')
            make('clean')
