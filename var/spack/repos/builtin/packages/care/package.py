# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Care(CMakePackage, CudaPackage, ROCmPackage):
    """
    Algorithms for chai managed arrays.
    """

    homepage = "https://github.com/LLNL/CARE"
    git      = "https://github.com/LLNL/CARE.git"

    version('develop', branch='develop', submodules='True')
    version('master', branch='main', submodules='True')
    version('0.3.0', tag='v0.3.0', submodules='True')
    version('0.2.0', tag='v0.2.0', submodules='True')

    variant('openmp', default=False, description='Build Shared Libs')
    variant('implicit_conversions', default=True, description='Enable implicit'
            'conversions to/from raw pointers')
    variant('benchmarks', default=True, description='Build benchmarks.')
    variant('examples', default=True, description='Build examples.')
    variant('docs', default=False, description='Build documentation')
    variant('tests', default=False, description='Build tests')
    variant('loop_fuser', default=False, description='Enable loop fusion capability')

    depends_on('blt', type='build')
    depends_on('blt@0.3.7:', type='build', when='+rocm')

    depends_on('camp')
    depends_on('umpire@develop')
    depends_on('raja@develop')
    depends_on('chai@develop+enable_pick~benchmarks')

    # WARNING: this package currently only supports an internal cub
    # package. This will cause a race condition if compiled with another
    # package that uses cub. TODO: have all packages point to the same external
    # cub package.
    depends_on('camp+cuda', when='+cuda')
    depends_on('umpire+cuda~shared', when='+cuda')
    depends_on('cub', when='+cuda')
    depends_on('raja+cuda~openmp', when='+cuda')
    depends_on('chai+cuda~shared', when='+cuda')

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    depends_on('camp+rocm', when='+rocm')
    depends_on('umpire+rocm', when='+rocm')
    depends_on('raja+rocm~openmp', when='+rocm')
    depends_on('chai+rocm', when='+rocm')
    for val in ROCmPackage.amdgpu_targets:
        depends_on('camp amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('umpire amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('raja amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('chai amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)

    conflicts('+openmp', when='+rocm')
    conflicts('+openmp', when='+cuda')

    def cmake_args(self):
        spec = self.spec

        options = []
        options.append('-DBLT_SOURCE_DIR={0}'.format(spec['blt'].prefix))

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=' + spec['cuda'].prefix,
                '-DNVTOOLSEXT_DIR=' + spec['cuda'].prefix,
                '-DCUB_DIR=' + spec['cub'].prefix])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                # Please note that within care, CUDA_ARCH is assigned to -code
                # and likewise CUDA_CODE is assigned to -arch, so these are
                # intentionally flipped here.
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                options.append('-DCUDA_CODE=compute_{0}'.format(cuda_arch[0]))
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

        options.append('-DCARE_ENABLE_IMPLICIT_CONVERSIONS={0}'.format(
            'ON' if '+implicit_conversions' in spec else 'OFF'))

        options.append('-DCARE_ENABLE_LOOP_FUSER={0}'.format(
            'ON' if '+loop_fuser' in spec else 'OFF'))

        options.append('-DCAMP_DIR:PATH='
                       + spec['camp'].prefix.share.camp.cmake)
        options.append('-DUMPIRE_DIR:PATH='
                       + spec['umpire'].prefix.share.umpire.cmake)
        options.append('-DRAJA_DIR:PATH='
                       + spec['raja'].prefix.share.raja.cmake)
        options.append('-DCHAI_DIR:PATH='
                       + spec['chai'].prefix.share.chai.cmake)

        options.append('-DCARE_ENABLE_TESTS={0}'.format(
            'ON' if '+tests' in spec else 'OFF'))
        # For tests to work, we also need BLT_ENABLE_TESTS to be on.
        # This will take care of the gtest dependency. CARE developers should
        # consider consolidating these flags in the future.
        options.append('-DBLT_ENABLE_TESTS={0}'.format(
            'ON' if '+tests' in spec else 'OFF'))

        # There are both CARE_ENABLE_* and ENABLE_* variables in here because
        # one controls the BLT infrastructure and the other controls the CARE
        # infrastructure. The goal is to just be able to use the CARE_ENABLE_*
        # variables, but CARE isn't set up correctly for that yet.
        options.append('-DENABLE_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))

        options.append('-DENABLE_DOCS={0}'.format(
            'ON' if '+docs' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_DOCS={0}'.format(
            'ON' if '+docs' in spec else 'OFF'))

        return options
