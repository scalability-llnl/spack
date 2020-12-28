# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Ginkgo(CMakePackage, CudaPackage):
    """High-performance linear algebra library for manycore systems,
    with a focus on sparse solution of linear systems."""

    homepage = "https://ginkgo-project.github.io/"
    git      = "https://github.com/ginkgo-project/ginkgo.git"

    maintainers = ['tcojean', 'hartwiganzt']

    version('develop', branch='develop')
    version('master', branch='master')
    version('1.3.0', commit='4678668c66f634169def81620a85c9a20b7cec78')  # v1.3.0
    version('1.2.0', commit='b4be2be961fd5db45c3d02b5e004d73550722e31')  # v1.2.0
    version('1.1.1', commit='08d2c5200d3c78015ac8a4fd488bafe1e4240cf5')  # v1.1.1
    version('1.1.0', commit='b9bec8225442b3eb2a85a870efa112ab767a17fb')  # v1.1.0
    version('1.0.0', commit='45244641e0c2b19ba33aecd25153c0bddbcbe1a0')  # v1.0.0

    variant('shared', default=True, description='Build shared libraries')
    variant('full_optimizations', default=False, description='Compile with all optimizations')
    variant('openmp', default=sys.platform != 'darwin',  description='Build with OpenMP')
    variant('develtools', default=False, description='Compile with develtools enabled')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('hip', default=False, description='Compile Ginkgo with HIP support')

    depends_on('cmake@3.9:', type='build')
    depends_on('cuda@9:',    when='+cuda')

    depends_on('hip',       when='+hip')
    depends_on('hipsparse', type="link", when='+hip')
    depends_on('hipblas',   type="link", when='+hip')
    depends_on('rocrand',   type="link", when='@develop+hip')
    depends_on('rocthrust',   type="build", when='+hip')

    # Somehow, these dependencies not propagated by the HIP stack?
    depends_on('rocm-device-libs',   type="link", when='+hip')
    depends_on('comgr',   type="link", when='+hip')

    conflicts('%gcc@:5.2.9')
    conflicts("+hip", when="@:1.1.1")
    # The HIP packages from spack doen't seem to work well with CUDA
    # backend for now, so disable HIP with CUDA backend.
    conflicts("+cuda", when="+hip")

    def cmake_args(self):
        # Check that the have the correct C++ standard is available
        if self.spec.satisfies('@:1.2.0'):
            try:
                self.compiler.cxx11_flag
            except UnsupportedCompilerFlag:
                InstallError('Ginkgo requires a C++11-compliant C++ compiler')
        else:
            try:
                self.compiler.cxx14_flag
            except UnsupportedCompilerFlag:
                InstallError('Ginkgo requires a C++14-compliant C++ compiler')

        spec = self.spec
        args = [
            '-DGINKGO_BUILD_CUDA=%s' % ('ON' if '+cuda' in spec else 'OFF'),
            '-DGINKGO_BUILD_OMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DGINKGO_JACOBI_FULL_OPTIMIZATIONS=%s' % (
                'ON' if '+full_optimizations' in spec else 'OFF'),
            '-DGINKGO_DEVEL_TOOLS=%s' % (
                'ON' if '+develtools' in spec else 'OFF'),
            '-DGINKGO_BUILD_HIP=%s' % ('ON' if '+hip' in spec else 'OFF'),
            # As we are not exposing benchmarks, examples, tests nor doc
            # as part of the installation, disable building them altogether.
            '-DGINKGO_BUILD_BENCHMARKS=OFF',
            '-DGINKGO_BUILD_DOC=OFF',
            '-DGINKGO_BUILD_EXAMPLES=OFF',
            '-DGINKGO_BUILD_TESTS=OFF'
        ]
        if '+hip' in spec:
            args.append('-DHIP_PATH={0}'. format(spec['hip'].prefix))
            args.append('-DHIP_CLANG_PATH={0}/bin'.
                        format(spec['llvm-amdgpu'].prefix))
            args.append('-DHIP_CLANG_INCLUDE_PATH={0}/include'.
                        format(spec['llvm-amdgpu'].prefix))
            args.append('-DHIPSPARSE_PATH={0}'.
                        format(spec['hipsparse'].prefix))
            args.append('-DHIPBLAS_PATH={0}'.
                        format(spec['hipblas'].prefix))
        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        """Perform smoke tests on the installed package."""
        with working_dir(self.build_directory):
            make("test_install")
