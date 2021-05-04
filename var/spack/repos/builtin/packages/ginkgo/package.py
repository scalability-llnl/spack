# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Ginkgo(CMakePackage, CudaPackage, ROCmPackage):
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
    variant('hwloc', default=False, description='Enable HWLOC support')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('cmake@3.9:', type='build')
    depends_on('cuda@9:',    when='+cuda')

    depends_on('rocthrust',  type="build", when='+rocm')
    depends_on('hipsparse',  type="link", when='+rocm')
    depends_on('hipblas',    type="link", when='+rocm')
    depends_on('rocrand',    type="link", when='+rocm')
    depends_on('hwloc@2.1:', type="link", when='+hwloc')

    depends_on('googletest', type="test")
    depends_on('numactl',    type="test", when="+hwloc")

    conflicts('%gcc@:5.2.9')
    conflicts("+rocm", when="@:1.1.1")
    conflicts("+cuda", when="+rocm")

    # ROCm 4.1.0 breaks platform settings which breaks Ginkgo's HIP support.
    conflicts("^hip@4.1.0:", when="@:1.3.0")
    conflicts("^hip@4.1.0:", when="@master")
    conflicts("^hipblas@4.1.0:", when="@:1.3.0")
    conflicts("^hipblas@4.1.0:", when="@master")
    conflicts("^hipsparse@4.1.0:", when="@:1.3.0")
    conflicts("^hipsparse@4.1.0:", when="@master")
    conflicts("^rocthrust@4.1.0:", when="@:1.3.0")
    conflicts("^rocthrust@4.1.0:", when="@master")

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
            '-DGINKGO_BUILD_HIP=%s' % ('ON' if '+rocm' in spec else 'OFF'),
            '-DGINKGO_BUILD_OMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DGINKGO_JACOBI_FULL_OPTIMIZATIONS=%s' % (
                'ON' if '+full_optimizations' in spec else 'OFF'),
            '-DGINKGO_BUILD_HWLOC=%s' % ('ON' if '+hwloc' in spec else 'OFF'),
            '-DGINKGO_DEVEL_TOOLS=%s' % (
                'ON' if '+develtools' in spec else 'OFF'),
            # As we are not exposing benchmarks, examples, tests nor doc
            # as part of the installation, disable building them altogether.
            '-DGINKGO_BUILD_BENCHMARKS=OFF',
            '-DGINKGO_BUILD_DOC=OFF',
            '-DGINKGO_BUILD_EXAMPLES=OFF',
            '-DGINKGO_BUILD_TESTS=%s' % ('ON' if self.run_tests else 'OFF'),
            # Let spack handle the RPATH
            '-DGINKGO_INSTALL_RPATH=OFF'
        ]

        if self.run_tests:
            args.append('-DGINKGO_USE_EXTERNAL_GTEST=ON')

        if '+cuda' in spec:
            archs = spec.variants['cuda_arch'].value
            if archs != 'none':
                arch_str = ";".join(archs)
                args.append('-DGINKGO_CUDA_ARCHITECTURES={0}'.format(arch_str))

        if '+rocm' in spec:
            args.append('-DHIP_PATH={0}'. format(spec['hip'].prefix))
            args.append('-DHIP_CLANG_PATH={0}/bin'.
                        format(spec['llvm-amdgpu'].prefix))
            args.append('-DHIP_CLANG_INCLUDE_PATH={0}/include'.
                        format(spec['llvm-amdgpu'].prefix))
            args.append('-DHIPSPARSE_PATH={0}'.
                        format(spec['hipsparse'].prefix))
            args.append('-DHIPBLAS_PATH={0}'.
                        format(spec['hipblas'].prefix))
            args.append('-DHIPRAND_PATH={0}/hiprand'.
                        format(spec['rocrand'].prefix))
            args.append('-DROCRAND_PATH={0}/rocrand'.
                        format(spec['rocrand'].prefix))
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ";".join(archs)
                args.append(
                    '-DGINKGO_HIP_AMDGPU={0}'.format(arch_str)
                )
        return args

    @run_after('install')
    def setup_build_tests(self):
        """Build and install the smoke tests."""
        # For now only develop and next releases support this scheme.
        if not self.spec.satisfies('@develop') and not self.spec.satisfies('@1.4.0:'):
            return
        with working_dir(self.build_directory):
            make("test_install")
        smoke_test_path = join_path(self.build_directory, 'test_install')
        with working_dir(smoke_test_path):
            make("install")

    def test(self):
        """Run the smoke tests."""
        # For now only develop and next releases support this scheme.
        if not self.spec.satisfies('@develop') and not self.spec.satisfies('@1.4.0:'):
            print("SKIPPED: smoke tests not supported with this Ginkgo version.")
            return
        files = [('test_install', [r'REFERENCE',
                                   r'correctly detected and is complete']),
                 ('test_install_cuda', [r'CUDA',
                                        r'correctly detected and is complete']),
                 ('test_install_hip', [r'HIP',
                                       r'correctly detected and is complete'])]
        smoke_test_path = join_path(self.prefix, 'smoke_tests')
        for f, expected in files:
            self.run_test(f, [], expected, skip_missing=True, installed=True,
                          work_dir=smoke_test_path)
