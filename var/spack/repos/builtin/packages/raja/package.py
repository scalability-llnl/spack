# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Raja(CMakePackage, CudaPackage, ROCmPackage):
    """RAJA Parallel Framework."""

    homepage = "http://software.llnl.gov/RAJA/"
    git      = "https://github.com/LLNL/RAJA.git"

    version('develop', branch='develop', submodules='True')
    version('main',  branch='main',  submodules='True')
    version('0.13.0', tag='v0.13.0', submodules='True')
    version('0.12.1', tag='v0.12.1', submodules="True")
    version('0.12.0', tag='v0.12.0', submodules="True")
    version('0.11.0', tag='v0.11.0', submodules="True")
    version('0.10.1', tag='v0.10.1', submodules="True")
    version('0.10.0', tag='v0.10.0', submodules="True")
    version('0.9.0', tag='v0.9.0', submodules="True")
    version('0.8.0', tag='v0.8.0', submodules="True")
    version('0.7.0', tag='v0.7.0', submodules="True")
    version('0.6.0', tag='v0.6.0', submodules="True")
    version('0.5.3', tag='v0.5.3', submodules="True")
    version('0.5.2', tag='v0.5.2', submodules="True")
    version('0.5.1', tag='v0.5.1', submodules="True")
    version('0.5.0', tag='v0.5.0', submodules="True")
    version('0.4.1', tag='v0.4.1', submodules="True")
    version('0.4.0', tag='v0.4.0', submodules="True")

    variant('openmp', default=True, description='Build OpenMP backend')
    variant('shared', default=True, description='Build Shared Libs')
    variant('examples', default=True, description='Build examples.')
    variant('exercises', default=True, description='Build exercises.')
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant('tests', default=False, description='Build tests')

    depends_on('blt', type='build')
    depends_on('blt@0.3.7:', type='build', when='+rocm')

    depends_on('camp')
    depends_on('camp+cuda', when='+cuda')

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    depends_on('camp+rocm', when='+rocm')
    for val in ROCmPackage.amdgpu_targets:
        depends_on('camp amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)

    conflicts('+openmp', when='+rocm')

    def cmake_args(self):
        spec = self.spec

        options = []

        options.append('-DBLT_SOURCE_DIR={0}'.format(spec['blt'].prefix))

        options.append('-DENABLE_OPENMP={0}'.format(
            'ON' if '+openmp' in spec else 'OFF'))

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
        else:
            options.append('-DENABLE_CUDA=OFF')

        if '+rocm' in spec:
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix)])
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                options.append(
                    '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.format(arch_str)
                )
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DBUILD_SHARED_LIBS={0}'.format(
            'ON' if '+shared' in spec else 'OFF'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))

        options.append('-DENABLE_EXERCISES={0}'.format(
            'ON' if '+exercises' in spec else 'OFF'))

        # Work around spack adding -march=ppc64le to SPACK_TARGET_ARGS which
        # is used by the spack compiler wrapper.  This can go away when BLT
        # removes -Werror from GTest flags
        if self.spec.satisfies('%clang target=ppc64le:') or not self.run_tests:
            options.append('-DENABLE_TESTS=OFF')
        else:
            options.append('-DENABLE_TESTS={0}'.format(
                'ON' if '+tests' in spec else 'OFF'))

        return options

    @property
    def build_relpath(self):
        """Relative path to the cmake build subdirectory."""
        return join_path('..', self.build_dirname)

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to a
        relative install test subdirectory for use during `spack test run`."""
        # Now copy the relative files
        self.cache_extra_test_sources(self.build_relpath)

        # Ensure the path exists since relying on a relative path at the
        # same level as the normal stage source path.
        mkdirp(self.install_test_root)

    @property
    def _extra_tests_path(self):
        # TODO: The tests should be converted to re-build and run examples
        # TODO: using the installed libraries.
        return join_path(self.install_test_root, self.build_relpath, 'bin')

    def _test_examples(self):
        """Perform very basic checks on a subset of copied examples."""
        checks = [
            ('ex5_line-of-sight_solution',
             [r'RAJA sequential', r'RAJA OpenMP', r'result -- PASS']),
            ('ex6_stencil-offset-layout_solution',
             [r'RAJA Views \(permuted\)', r'result -- PASS']),
            ('ex8_tiled-matrix-transpose_solution',
             [r'parallel top inner loop',
              r'collapsed inner loops', r'result -- PASS']),
            ('kernel-dynamic-tile', [r'Running index', r'(24,24)']),
            ('plugin-example',
             [r'Launching host kernel for the 10 time']),
            ('tut_batched-matrix-multiply', [r'result -- PASS']),
            ('wave-eqn', [r'Max Error = 2', r'Evolved solution to time'])
        ]
        for exe, expected in checks:
            reason = 'test: checking output of {0} for {1}' \
                .format(exe, expected)
            self.run_test(exe, [], expected, installed=False,
                          purpose=reason, skip_missing=True,
                          work_dir=self._extra_tests_path)

    def test(self):
        """Perform smoke tests."""
        self._test_examples()
