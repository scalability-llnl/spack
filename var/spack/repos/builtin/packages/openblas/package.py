# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack import *
from spack.package_test import compare_output_file, compile_c_and_execute


class Openblas(MakefilePackage):
    """OpenBLAS: An optimized BLAS library"""

    homepage = 'https://www.openblas.net'
    url      = 'https://github.com/xianyi/OpenBLAS/archive/v0.2.19.tar.gz'
    git      = 'https://github.com/xianyi/OpenBLAS.git'

    version('develop', branch='develop')
    version('0.3.14', sha256='d381935d26f9cae8e4bbd7d7f278435adf8e3a90920edf284bb9ad789ee9ad60')
    version('0.3.13', sha256='79197543b17cc314b7e43f7a33148c308b0807cd6381ee77f77e15acf3e6459e')
    version('0.3.12', sha256='65a7d3a4010a4e3bd5c0baa41a234797cd3a1735449a4a5902129152601dc57b')
    version('0.3.11', sha256='bc4617971179e037ae4e8ebcd837e46db88422f7b365325bd7aba31d1921a673')
    version('0.3.10', sha256='0484d275f87e9b8641ff2eecaa9df2830cbe276ac79ad80494822721de6e1693')
    version('0.3.9', sha256='17d4677264dfbc4433e97076220adc79b050e4f8a083ea3f853a53af253bc380')
    version('0.3.8', sha256='8f86ade36f0dbed9ac90eb62575137388359d97d8f93093b38abe166ad7ef3a8')
    version('0.3.7', sha256='bde136122cef3dd6efe2de1c6f65c10955bbb0cc01a520c2342f5287c28f9379')
    version('0.3.6', sha256='e64c8fe083832ffbc1459ab6c72f71d53afd3b36e8497c922a15a06b72e9002f')
    version('0.3.5', sha256='0950c14bd77c90a6427e26210d6dab422271bc86f9fc69126725833ecdaa0e85')
    version('0.3.4', sha256='4b4b4453251e9edb5f57465bf2b3cf67b19d811d50c8588cdf2ea1f201bb834f')
    version('0.3.3', sha256='49d88f4494ae780e3d7fa51769c00d982d7cdb73e696054ac3baa81d42f13bab')
    version('0.3.2', sha256='e8ba64f6b103c511ae13736100347deb7121ba9b41ba82052b1a018a65c0cb15')
    version('0.3.1', sha256='1f5e956f35f3acdd3c74516e955d797a320c2e0135e31d838cbdb3ea94d0eb33')
    version('0.3.0',  sha256='cf51543709abe364d8ecfb5c09a2b533d2b725ea1a66f203509b21a8e9d8f1a1')
    version('0.2.20', sha256='5ef38b15d9c652985774869efd548b8e3e972e1e99475c673b25537ed7bcf394')
    version('0.2.19', sha256='9c40b5e4970f27c5f6911cb0a28aa26b6c83f17418b69f8e5a116bb983ca8557')
    version('0.2.18', sha256='7d9f8d4ea4a65ab68088f3bb557f03a7ac9cb5036ef2ba30546c3a28774a4112')
    version('0.2.17', sha256='0fe836dfee219ff4cadcc3567fb2223d9e0da5f60c7382711fb9e2c35ecf0dbf')
    version('0.2.16', sha256='766f350d0a4be614812d535cead8c816fc3ad3b9afcd93167ea5e4df9d61869b')
    version('0.2.15', sha256='73c40ace5978282224e5e122a41c8388c5a19e65a6f2329c2b7c0b61bacc9044')

    variant('ilp64', default=False, description='Force 64-bit Fortran native integers')
    variant('pic', default=True, description='Build position independent code')
    variant('shared', default=True, description='Build shared libraries')
    variant('consistent_fpcsr', default=False, description='Synchronize FP CSR between threads (x86/x86_64 only)')
    variant('bignuma', default=False, description='Enable experimental support for up to 1024 CPUs/Cores and 128 numa nodes')

    variant('locking', default=True, description='Build with thread safety')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    # virtual dependency
    provides('blas')
    provides('lapack')

    # OpenBLAS >=3.0 has an official way to disable internal parallel builds
    patch('make.patch', when='@0.2.16:0.2.20')
    #  This patch is in a pull request to OpenBLAS that has not been handled
    #  https://github.com/xianyi/OpenBLAS/pull/915
    #  UPD: the patch has been merged starting version 0.2.20
    patch('openblas_icc.patch', when='@:0.2.19%intel')
    patch('openblas_icc_openmp.patch', when='@:0.2.20%intel@16.0:')
    patch('openblas_icc_fortran.patch', when='%intel@16.0:')
    patch('openblas_icc_fortran2.patch', when='%intel@18.0:')
    # See https://github.com/spack/spack/issues/15385
    patch('lapack-0.3.9-xerbl.patch', when='@0.3.8:0.3.9 %intel')

    # Fixes compilation error on POWER8 with GCC 7
    # https://github.com/xianyi/OpenBLAS/pull/1098
    patch('power8.patch', when='@0.2.18:0.2.19 %gcc@7.1.0: target=power8')

    # Change file comments to work around clang 3.9 assembler bug
    # https://github.com/xianyi/OpenBLAS/pull/982
    patch('openblas0.2.19.diff', when='@0.2.19')

    # Fix CMake export symbol error
    # https://github.com/xianyi/OpenBLAS/pull/1703
    patch('openblas-0.3.2-cmake.patch', when='@0.3.1:0.3.2')

    # Disable experimental TLS code that lead to many threading issues
    # https://github.com/xianyi/OpenBLAS/issues/1735#issuecomment-422954465
    # https://github.com/xianyi/OpenBLAS/issues/1761#issuecomment-421039174
    # https://github.com/xianyi/OpenBLAS/pull/1765
    patch('https://github.com/xianyi/OpenBLAS/commit/4d183e5567346f80f2ef97eb98f8601c47f8cb56.patch',
          sha256='714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33',
          when='@0.3.3')

    # Fix parallel build issues on filesystems
    # with missing sub-second timestamp resolution
    patch('https://github.com/xianyi/OpenBLAS/commit/79ea839b635d1fd84b6ce8a47e086f01d64198e6.patch',
          sha256='f1b066a4481a50678caeb7656bf3e6764f45619686ac465f257c8017a2dc1ff0',
          when='@0.3.0:0.3.3')

    # Fix https://github.com/xianyi/OpenBLAS/issues/2431
    # Patch derived from https://github.com/xianyi/OpenBLAS/pull/2424
    patch('openblas-0.3.8-darwin.patch', when='@0.3.8 platform=darwin')
    # Fix ICE in LLVM 9.0.0 https://github.com/xianyi/OpenBLAS/pull/2329
    # Patch as in https://github.com/xianyi/OpenBLAS/pull/2597
    patch('openblas_appleclang11.patch', when='@0.3.8:0.3.9 %apple-clang@11.0.3')
    # There was an error in Reference-LAPACK that is triggeret by Xcode12
    # fixed upstream by https://github.com/xianyi/OpenBLAS/pull/2808 and
    # should be included in post 0.3.10 versions. Application to earlier
    # versions was not tested.
    # See also https://github.com/xianyi/OpenBLAS/issues/2870
    patch('https://github.com/xianyi/OpenBLAS/commit/f42e84d46c52f4ee1e05af8f365cd85de8a77b95.patch',
          sha256='7b1eec78d1b1f55d3a3f1249696be7da0e2e1cd3b7fadae852e97dc860f8a7fd',
          when='@0.3.8:0.3.10 %apple-clang@12.0.0:')

    # Add conditions to f_check to determine the Fujitsu compiler
    # See https://github.com/xianyi/OpenBLAS/pull/3010
    # UPD: the patch has been merged starting version 0.3.13
    patch('openblas_fujitsu.patch', when='@:0.3.10 %fj')
    patch('openblas_fujitsu_v0.3.11.patch', when='@0.3.11:0.3.12 %fj')
    patch('openblas_fujitsu2.patch', when='@0.3.10:0.3.12 %fj')

    # Use /usr/bin/env perl in build scripts
    patch('0001-use-usr-bin-env-perl.patch', when='@:0.3.13')

    # See https://github.com/spack/spack/issues/19932#issuecomment-733452619
    conflicts('%gcc@7.0.0:7.3.99,8.0.0:8.2.99', when='@0.3.11:')

    # See https://github.com/xianyi/OpenBLAS/issues/3074
    conflicts('%gcc@:10.1.99', when='@0.3.13 target=ppc64le:')

    # See https://github.com/spack/spack/issues/3036
    conflicts('%intel@16', when='@0.2.15:0.2.19')
    conflicts('+consistent_fpcsr', when='threads=none',
              msg='FPCSR consistency only applies to multithreading')

    conflicts('threads=pthreads', when='~locking', msg='Pthread support requires +locking')
    conflicts('threads=openmp', when='%apple-clang', msg="Apple's clang does not support OpenMP")
    conflicts('threads=openmp @:0.2.19', when='%clang', msg='OpenBLAS @:0.2.19 does not support OpenMP with clang!')

    depends_on('perl', type='build')

    @property
    def parallel(self):
        # unclear whether setting `-j N` externally was supported before 0.3
        return self.spec.version >= Version('0.3.0')

    @run_before('edit')
    def check_compilers(self):
        # As of 06/2016 there is no mechanism to specify that packages which
        # depends on Blas/Lapack need C or/and Fortran symbols. For now
        # require both.
        if self.compiler.fc is None:
            raise InstallError(
                'OpenBLAS requires both C and Fortran compilers!'
            )

    @staticmethod
    def _read_targets(target_file):
        """Parse a list of available targets from the OpenBLAS/TargetList.txt
        file.
        """
        micros = []
        re_target = re.compile(r'^[A-Z0-9_]+$')
        for line in target_file:
            match = re_target.match(line)
            if match is not None:
                micros.append(line.strip().lower())

        return micros

    def _microarch_target_args(self):
        """Given a spack microarchitecture and a list of targets found in
        OpenBLAS' TargetList.txt, determine the best command-line arguments.
        """
        # Read available openblas targets
        targetlist_name = join_path(self.stage.source_path, "TargetList.txt")
        if os.path.exists(targetlist_name):
            with open(targetlist_name) as f:
                available_targets = self._read_targets(f)
        else:
            available_targets = []

        # Get our build microarchitecture
        microarch = self.spec.target

        # List of arguments returned by this function
        args = []

        # List of available architectures, and possible aliases
        openblas_arch = set(['alpha', 'arm', 'ia64', 'mips', 'mips64',
                             'power', 'sparc', 'zarch'])
        openblas_arch_map = {
            'amd64': 'x86_64',
            'powerpc64': 'power',
            'i386': 'x86',
            'aarch64': 'arm64',
        }
        openblas_arch.update(openblas_arch_map.keys())
        openblas_arch.update(openblas_arch_map.values())

        # Add spack-only microarchitectures to list
        skylake = set(["skylake", "skylake_avx512"])
        available_targets = set(available_targets) | skylake | openblas_arch

        # Find closest ancestor that is known to build in blas
        if microarch.name not in available_targets:
            for microarch in microarch.ancestors:
                if microarch.name in available_targets:
                    break

        if self.version >= Version("0.3"):
            # 'ARCH' argument causes build errors in older OpenBLAS
            # see https://github.com/spack/spack/issues/15385
            arch_name = microarch.family.name
            if arch_name in openblas_arch:
                # Apply possible spack->openblas arch name mapping
                arch_name = openblas_arch_map.get(arch_name, arch_name)
                args.append('ARCH=' + arch_name)

        if microarch.vendor == 'generic':
            # User requested a generic platform, or we couldn't find a good
            # match for the requested one. Allow OpenBLAS to determine
            # an optimized kernel at run time, including older CPUs, while
            # forcing it not to add flags for the current host compiler.
            args.append('DYNAMIC_ARCH=1')
            if self.spec.version >= Version('0.3.12'):
                # These are necessary to prevent OpenBLAS from targeting the
                # host architecture on newer version of OpenBLAS, but they
                # cause build errors on 0.3.5 .
                args.extend(['DYNAMIC_OLDER=1', 'TARGET=GENERIC'])

        elif microarch.name in skylake:
            # Special case for renaming skylake family
            args.append('TARGET=SKYLAKEX')
            if microarch.name == "skylake":
                # Special case for disabling avx512 instructions
                args.append('NO_AVX512=1')
        else:
            args.append('TARGET=' + microarch.name.upper())

        return args

    @property
    def make_defs(self):
        # Configure fails to pick up fortran from FC=/abs/path/to/fc, but
        # works fine with FC=/abs/path/to/gfortran.
        # When mixing compilers make sure that
        # $SPACK_ROOT/lib/spack/env/<compiler> have symlinks with reasonable
        # names and hack them inside lib/spack/spack/compilers/<compiler>.py
        make_defs = [
            'CC={0}'.format(spack_cc),
            'FC={0}'.format(spack_fc),
        ]

        # force OpenBLAS to use externally defined parallel build
        if self.spec.version < Version('0.3'):
            make_defs.append('MAKE_NO_J=1')  # flag defined by our make.patch
        else:
            make_defs.append('MAKE_NB_JOBS=0')  # flag provided by OpenBLAS

        # Add target and architecture flags
        make_defs += self._microarch_target_args()

        if '~shared' in self.spec:
            if '+pic' in self.spec:
                make_defs.extend([
                    'CFLAGS={0}'.format(self.compiler.cc_pic_flag),
                    'FFLAGS={0}'.format(self.compiler.f77_pic_flag)
                ])
            make_defs += ['NO_SHARED=1']
        # fix missing _dggsvd_ and _sggsvd_
        if self.spec.satisfies('@0.2.16'):
            make_defs += ['BUILD_LAPACK_DEPRECATED=1']

        # serial, but still thread-safe version
        if self.spec.satisfies('@0.3.7:'):
            if '+locking' in self.spec:
                make_defs += ['USE_LOCKING=1']
            else:
                make_defs += ['USE_LOCKING=0']

        # Add support for multithreading
        if self.spec.satisfies('threads=openmp'):
            make_defs += ['USE_OPENMP=1', 'USE_THREAD=1']
        elif self.spec.satisfies('threads=pthreads'):
            make_defs += ['USE_OPENMP=0', 'USE_THREAD=1']
        else:
            make_defs += ['USE_OPENMP=0', 'USE_THREAD=0']

        # 64bit ints
        if '+ilp64' in self.spec:
            make_defs += ['INTERFACE64=1']

        # Synchronize floating-point control and status register (FPCSR)
        # between threads (x86/x86_64 only).
        if '+consistent_fpcsr' in self.spec:
            make_defs += ['CONSISTENT_FPCSR=1']

        # Flang/f18 does not provide ETIME as an intrinsic
        if self.spec.satisfies('%clang'):
            make_defs.append('TIMER=INT_CPU_TIME')

        # Prevent errors in `as` assembler from newer instructions
        if self.spec.satisfies('%gcc@:4.8.4'):
            make_defs.append('NO_AVX2=1')

        # Fujitsu Compiler dose not add  Fortran runtime in rpath.
        if self.spec.satisfies('%fj'):
            make_defs.append('LDFLAGS=-lfj90i -lfj90f -lfjsrcinfo -lelf')

        # Newer versions of openblas will try to find ranlib in the compiler's
        # prefix, for instance, .../lib/spack/env/gcc/ranlib, which will fail.
        if self.spec.satisfies('@0.3.13:'):
            make_defs.append('RANLIB=ranlib')

        if self.spec.satisfies('+bignuma'):
            make_defs.append('BIGNUMA=1')

        return make_defs

    @property
    def headers(self):
        # As in netlib-lapack, the only public headers for cblas and lapacke in
        # openblas are cblas.h and lapacke.h. The remaining headers are private
        # headers either included in one of these two headers, or included in
        # one of the source files implementing functions declared in these
        # headers.
        return find_headers(['cblas', 'lapacke'], self.prefix.include)

    @property
    def build_targets(self):
        targets = ['libs', 'netlib']

        # Build shared if variant is set.
        if '+shared' in self.spec:
            targets += ['shared']

        return self.make_defs + targets

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make('tests', *self.make_defs, parallel=False)

    @property
    def install_targets(self):
        make_args = [
            'install',
            'PREFIX={0}'.format(self.prefix),
        ]
        return make_args + self.make_defs

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        spec = self.spec
        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small
        # test.
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = spec['openblas'].headers.cpp_flags
        link_flags = spec['openblas'].libs.ld_flags
        if self.compiler.name == 'intel':
            link_flags += ' -lifcore'
        if self.spec.satisfies('threads=pthreads'):
            link_flags += ' -lpthread'
        if spec.satisfies('threads=openmp'):
            link_flags += ' -lpthread ' + self.compiler.openmp_flag

        output = compile_c_and_execute(
            source_file, [include_flags], link_flags.split()
        )
        compare_output_file(output, blessed_file)
