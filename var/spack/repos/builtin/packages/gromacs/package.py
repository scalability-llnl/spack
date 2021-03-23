# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class Gromacs(CMakePackage):
    """GROMACS (GROningen MAchine for Chemical Simulations) is a molecular
    dynamics package primarily designed for simulations of proteins, lipids
    and nucleic acids. It was originally developed in the Biophysical
    Chemistry department of University of Groningen, and is now maintained
    by contributors in universities and research centers across the world.

    GROMACS is one of the fastest and most popular software packages
    available and can run on CPUs as well as GPUs. It is free, open source
    released under the GNU General Public License. Starting from version 4.6,
    GROMACS is released under the GNU Lesser General Public License.
    """

    homepage = 'http://www.gromacs.org'
    url      = 'http://ftp.gromacs.org/gromacs/gromacs-5.1.2.tar.gz'
    git      = 'https://github.com/gromacs/gromacs.git'
    maintainers = ['junghans', 'marvinbernhardt']

    version('master', branch='master')
    version('2021', sha256='efa78ab8409b0f5bf0fbca174fb8fbcf012815326b5c71a9d7c385cde9a8f87b')
    version('2020.5', sha256='7b6aff647f7c8ee1bf12204d02cef7c55f44402a73195bd5f42cf11850616478')
    version('2020.4', sha256='5519690321b5500c7951aaf53ff624042c3edd1a5f5d6dd1f2d802a3ecdbf4e6')
    version('2020.3', sha256='903183691132db14e55b011305db4b6f4901cc4912d2c56c131edfef18cc92a9')
    version('2020.2', sha256='7465e4cd616359d84489d919ec9e4b1aaf51f0a4296e693c249e83411b7bd2f3')
    version('2020.1', sha256='e1666558831a3951c02b81000842223698016922806a8ce152e8f616e29899cf')
    version('2020', sha256='477e56142b3dcd9cb61b8f67b24a55760b04d1655e8684f979a75a5eec40ba01')
    version('2019.6', sha256='bebe396dc0db11a9d4cc205abc13b50d88225617642508168a2195324f06a358')
    version('2019.5', sha256='438061a4a2d45bbb5cf5c3aadd6c6df32d2d77ce8c715f1c8ffe56156994083a')
    version('2019.4', sha256='ba4366eedfc8a1dbf6bddcef190be8cd75de53691133f305a7f9c296e5ca1867')
    version('2019.3', sha256='4211a598bf3b7aca2b14ad991448947da9032566f13239b1a05a2d4824357573')
    version('2019.2', sha256='bcbf5cc071926bc67baa5be6fb04f0986a2b107e1573e15fadcb7d7fc4fb9f7e')
    version('2019.1', sha256='b2c37ed2fcd0e64c4efcabdc8ee581143986527192e6e647a197c76d9c4583ec')
    version('2019', sha256='c5b281a5f0b5b4eeb1f4c7d4dc72f96985b566561ca28acc9c7c16f6ee110d0b')
    version('2018.8', sha256='776923415df4bc78869d7f387c834141fdcda930b2e75be979dc59ecfa6ebecf')
    version('2018.5', sha256='32261df6f7ec4149fc0508f9af416953d056e281590359838c1ed6644ba097b8')
    version('2018.4', sha256='6f2ee458c730994a8549d6b4f601ecfc9432731462f8bd4ffa35d330d9aaa891')
    version('2018.3', sha256='4423a49224972969c52af7b1f151579cea6ab52148d8d7cbae28c183520aa291')
    version('2018.2', sha256='4bdde8120c510b6543afb4b18f82551fddb11851f7edbd814aa24022c5d37857')
    version('2018.1', sha256='4d3533340499323fece83b4a2d4251fa856376f2426c541e00b8e6b4c0d705cd')
    version('2018',   sha256='deb5d0b749a52a0c6083367b5f50a99e08003208d81954fb49e7009e1b1fd0e9')
    version('2016.6', sha256='bac0117d2cad21f9b94fe5b854fb9ae7435b098a6da4e732ee745f18e52473d7')
    version('2016.5', sha256='57db26c6d9af84710a1e0c47a1f5bf63a22641456448dcd2eeb556ebd14e0b7c')
    version('2016.4', sha256='4be9d3bfda0bdf3b5c53041e0b8344f7d22b75128759d9bfa9442fe65c289264')
    version('2016.3', sha256='7bf00e74a9d38b7cef9356141d20e4ba9387289cbbfd4d11be479ef932d77d27')
    version('5.1.5',  sha256='c25266abf07690ecad16ed3996899b1d489cbb1ef733a1befb3b5c75c91a703e')
    version('5.1.4',  sha256='0f3793d8f1f0be747cf9ebb0b588fb2b2b5dc5acc32c3046a7bee2d2c03437bc')
    version('5.1.2',  sha256='39d6f1d7ae8ba38cea6089da40676bfa4049a49903d21551abc030992a58f304')
    version('4.5.5', sha256='e0605e4810b0d552a8761fef5540c545beeaf85893f4a6e21df9905a33f871ba')

    variant('mpi', default=True, description='Activate MPI support')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant(
        'double', default=False,
        description='Produces a double precision version of the executables')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('opencl', default=False, description='Enable OpenCL support')
    variant('sycl', default=False, description='Enable SYCL support')
    variant('nosuffix', default=False, description='Disable default suffixes')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel',
                    'Reference', 'RelWithAssert', 'Profile'))
    variant('mdrun_only', default=False,
            description='Enables the build of a cut-down version'
            ' of libgromacs and/or the mdrun program')
    conflicts('+mdrun_only', when='@2021:',
              msg='mdrun-only build option was removed for GROMACS 2021.')
    variant('openmp', default=True,
            description='Enables OpenMP at configure time')
    variant('relaxed_double_precision', default=False,
            description='GMX_RELAXED_DOUBLE_PRECISION, use only for Fujitsu PRIMEHPC')
    conflicts('+relaxed_double_precision', when='@2021:',
              msg='GMX_RELAXED_DOUBLE_PRECISION option removed for GROMACS 2021.')
    variant('hwloc', default=True,
            description='Use the hwloc portable hardware locality library')
    variant('lapack', default=False,
            description='Enables an external LAPACK library')
    variant('blas', default=False,
            description='Enables an external BLAS library')
    variant('cycle_subcounters', default=False,
            description='Enables cycle subcounters')

    depends_on('mpi', when='+mpi')
    # define matching plumed versions
    depends_on('plumed@2.6.0:2.6.9+mpi', when='@2020.2+plumed+mpi')
    depends_on('plumed@2.6.0:2.6.9~mpi', when='@2020.2+plumed~mpi')
    depends_on('plumed@2.6.0:2.6.9+mpi', when='@2019.6+plumed+mpi')
    depends_on('plumed@2.6.0:2.6.9~mpi', when='@2019.6+plumed~mpi')
    depends_on('plumed@2.5.0:2.5.9+mpi', when='@2019.4+plumed+mpi')
    depends_on('plumed@2.5.0:2.5.9~mpi', when='@2019.4+plumed~mpi')
    depends_on('plumed@2.5.0:2.5.9+mpi', when='@2018.6+plumed+mpi')
    depends_on('plumed@2.5.0:2.5.9~mpi', when='@2018.6+plumed~mpi')
    depends_on('plumed+mpi', when='+plumed+mpi')
    depends_on('plumed~mpi', when='+plumed~mpi')
    depends_on('fftw-api@3')
    depends_on('cmake@2.8.8:3.99.99', type='build')
    depends_on('cmake@3.4.3:3.99.99', type='build', when='@2018:')
    depends_on('cmake@3.9.6:3.99.99', type='build', when='@2020')
    depends_on('cmake@3.13.0:3.99.99', type='build', when='@2021:')
    depends_on('cmake@3.16.0:3.99.99', type='build', when='@master')
    depends_on('cmake@3.16.0:3.99.99', type='build', when='%fj')
    depends_on('cuda', when='+cuda')
    depends_on('sycl', when='+sycl')
    depends_on('lapack', when='+lapack')
    depends_on('blas', when='+blas')

    depends_on('hwloc', when='+hwloc')

    patch('gmxDetectCpu-cmake-3.14.patch', when='@2018:2019.3^cmake@3.14.0:')
    patch('gmxDetectSimd-cmake-3.14.patch', when='@:2017.99^cmake@3.14.0:')

    filter_compiler_wrappers(
        '*.cmake',
        relative_root=os.path.join('share', 'cmake', 'gromacs_mpi'))
    filter_compiler_wrappers(
        '*.cmake',
        relative_root=os.path.join('share', 'cmake', 'gromacs'))

    def patch(self):
        if '+plumed' in self.spec:
            self.spec['plumed'].package.apply_patch(self)

        if self.spec.satisfies('%nvhpc'):
            # Disable obsolete workaround
            filter_file('ifdef __PGI', 'if 0', 'src/gromacs/fileio/xdrf.h')

    def cmake_args(self):

        options = []

        if '+mpi' in self.spec:
            options.append('-DGMX_MPI:BOOL=ON')
            if self.version < Version('2020'):
                # Ensures gmxapi builds properly
                options.extend([
                    '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % self.spec['mpi'].mpifc,
                ])
            elif self.version == Version('2021'):
                # Work around https://gitlab.com/gromacs/gromacs/-/issues/3896
                # Ensures gmxapi builds properly
                options.extend([
                    '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
                ])
            else:
                options.extend([
                    '-DCMAKE_C_COMPILER=%s' % spack_cc,
                    '-DCMAKE_CXX_COMPILER=%s' % spack_cxx,
                    '-DMPI_C_COMPILER=%s' % self.spec['mpi'].mpicc,
                    '-DMPI_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx
                ])
        else:
            options.extend([
                '-DCMAKE_C_COMPILER=%s' % spack_cc,
                '-DCMAKE_CXX_COMPILER=%s' % spack_cxx,
                '-DGMX_MPI:BOOL=OFF'])

        if self.spec.satisfies('@2020:'):
            options.append('-DGMX_INSTALL_LEGACY_API=ON')

        if '+double' in self.spec:
            options.append('-DGMX_DOUBLE:BOOL=ON')

        if '+nosuffix' in self.spec:
            options.append('-DGMX_DEFAULT_SUFFIX:BOOL=OFF')

        if '~shared' in self.spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
            options.append('-DGMXAPI:BOOL=OFF')

        if '+hwloc' in self.spec:
            options.append('-DGMX_HWLOC:BOOL=ON')
        else:
            options.append('-DGMX_HWLOC:BOOL=OFF')

        if self.version >= Version('2021'):
            if '+cuda' in self.spec:
                options.append('-DGMX_GPU:STRING=CUDA')
            elif '+opencl' in self.spec:
                options.append('-DGMX_GPU:STRING=OpenCL')
            elif '+sycl' in self.spec:
                options.append('-DGMX_GPU:STRING=SYCL')
            else:
                options.append('-DGMX_GPU:STRING=OFF')
        else:
            if '+cuda' in self.spec or '+opencl' in self.spec:
                options.append('-DGMX_GPU:BOOL=ON')
            else:
                options.append('-DGMX_GPU:BOOL=OFF')

        if '+cuda' in self.spec:
            options.append('-DCUDA_TOOLKIT_ROOT_DIR:STRING=' +
                           self.spec['cuda'].prefix)

        if '+opencl' in self.spec:
            options.append('-DGMX_USE_OPENCL=on')

        if '+lapack' in self.spec:
            options.append('-DGMX_EXTERNAL_LAPACK:BOOL=ON')
            if self.spec['lapack'].libs:
                options.append('-DGMX_LAPACK_USER={0}'.format(
                    self.spec['lapack'].libs.joined(';')))
        else:
            options.append('-DGMX_EXTERNAL_LAPACK:BOOL=OFF')

        if '+blas' in self.spec:
            options.append('-DGMX_EXTERNAL_BLAS:BOOL=ON')
            if self.spec['blas'].libs:
                options.append('-DGMX_BLAS_USER={0}'.format(
                    self.spec['blas'].libs.joined(';')))
        else:
            options.append('-DGMX_EXTERNAL_BLAS:BOOL=OFF')

        # Activate SIMD based on properties of the target
        target = self.spec.target
        if target >= 'zen2':
            # AMD Family 17h (EPYC Rome)
            options.append('-DGMX_SIMD=AVX2_256')
        elif target >= 'zen':
            # AMD Family 17h (EPYC Naples)
            options.append('-DGMX_SIMD=AVX2_128')
        elif target >= 'bulldozer':
            # AMD Family 15h
            options.append('-DGMX_SIMD=AVX_128_FMA')
        elif 'vsx' in target:
            # IBM Power 7 and beyond
            options.append('-DGMX_SIMD=IBM_VSX')
        elif target.family == 'aarch64':
            # ARMv8
            if self.spec.satisfies('%nvhpc'):
                options.append('-DGMX_SIMD=None')
            else:
                options.append('-DGMX_SIMD=ARM_NEON_ASIMD')
        elif target == 'mic_knl':
            # Intel KNL
            options.append('-DGMX_SIMD=AVX_512_KNL')
        else:
            # Other architectures
            simd_features = [
                ('sse2', 'SSE2'),
                ('sse4_1', 'SSE4.1'),
                ('avx', 'AVX_256'),
                ('axv128', 'AVX2_128'),
                ('avx2', 'AVX2_256'),
                ('avx512', 'AVX_512'),
            ]

            # Workaround NVIDIA compiler bug when avx512 is enabled
            if (self.spec.satisfies('%nvhpc') and
                ('avx512', 'AVX_512') in simd_features):
                simd_features.remove(('avx512', 'AVX_512'))

            feature_set = False
            for feature, flag in reversed(simd_features):
                if feature in target:
                    options.append('-DGMX_SIMD:STRING={0}'.format(flag))
                    feature_set = True
                    break

            # Fall back
            if not feature_set:
                options.append('-DGMX_SIMD:STRING=None')

        # Use the 'rtdscp' assembly instruction only on
        # appropriate architectures
        options.append(self.define(
            'GMX_USE_RDTSCP', str(target.family) in ('x86_64', 'x86')
        ))

        if self.spec.satisfies('@:2020'):
            options.append(
                self.define_from_variant('GMX_BUILD_MDRUN_ONLY', 'mdrun_only'))

        options.append(self.define_from_variant('GMX_OPENMP', 'openmp'))

        if self.spec.satisfies('@:2020'):
            options.append(
                self.define_from_variant(
                    'GMX_RELAXED_DOUBLE_PRECISION',
                    'relaxed_double_precision'))

        if '+cycle_subcounters' in self.spec:
            options.append('-DGMX_CYCLE_SUBCOUNTERS:BOOL=ON')
        else:
            options.append('-DGMX_CYCLE_SUBCOUNTERS:BOOL=OFF')

        if '^mkl' in self.spec:
            # fftw-api@3 is provided by intel-mkl or intel-parllel-studio
            # we use the mkl interface of gromacs
            options.append('-DGMX_FFT_LIBRARY=mkl')
            options.append('-DMKL_INCLUDE_DIR={0}'.
                           format(self.spec['mkl'].headers.directories[0]))
            # The 'blas' property provides a minimal set of libraries
            # that is sufficient for fft. Using full mkl fails the cmake test
            options.append('-DMKL_LIBRARIES={0}'.
                           format(self.spec['blas'].libs.joined(';')))
        else:
            # we rely on the fftw-api@3
            options.append('-DGMX_FFT_LIBRARY=fftw3')
            if '^amdfftw' in self.spec:
                options.append('-DGMX_FFT_LIBRARY=fftw3')
                options.append(
                    '-DFFTWF_INCLUDE_DIRS={0}'.
                    format(self.spec['amdfftw'].headers.directories[0])
                )
                options.append('-DFFTWF_LIBRARIES={0}'.
                               format(self.spec['amdfftw'].libs.joined(';')))

        return options
