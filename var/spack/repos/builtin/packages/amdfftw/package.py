# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *
from spack.pkg.builtin.fftw import FftwBase


class Amdfftw(FftwBase):
    """FFTW (AMD Optimized version) is a comprehensive collection of
    fast C routines for computing the Discrete Fourier Transform (DFT)
    and various special cases thereof.

    It is an open-source implementation of the Fast Fourier transform
    algorithm. It can compute transforms of real and complex-values
    arrays of arbitrary size and dimension.
    AMD Optimized FFTW is the optimized FFTW implementation targeted
    for AMD CPUs.

    For single precision build, please use precision value as float.
    Example : spack install amdfftw precision=float
    """

    _name = 'amdfftw'
    homepage = "https://developer.amd.com/amd-aocl/fftw/"
    url = "https://github.com/amd/amd-fftw/archive/3.0.tar.gz"
    git = "https://github.com/amd/amd-fftw.git"

    maintainers = ['amd-toolchain-support']

    version('3.0', sha256='a69deaf45478a59a69f77c4f7e9872967f1cfe996592dd12beb6318f18ea0bcd')
    version('2.2', sha256='de9d777236fb290c335860b458131678f75aa0799c641490c644c843f0e246f8')

    variant('shared', default=True, description="Builds a shared version of the library")
    variant('openmp', default=True, description="Enable OpenMP support")
    variant('threads', default=False, description="Enable SMP threads support")
    variant('debug', default=False, description="Builds a debug version of the library")
    variant(
        'amd-fast-planner',
        default=False,
        description="Option to reduce the planning time without much"
                    "tradeoff in the performance. It is supported for"
                    "Float and double precisions only.")

    depends_on('texinfo')

    provides('fftw-api@3', when='@2:')

    conflicts('precision=quad', when='@2.2 %aocc', msg="AOCC clang doesn't support quad precision")
    conflicts('+debug', when='@2.2 %aocc', msg="AOCC clang doesn't support debug")
    conflicts('%gcc@:7.2', when="@2.2:", msg="Required GCC version above 7.2 for AMDFFTW")
    conflicts('+amd-fast-planner', when="@2.2", msg="amd-fast-planner is supported from 3.0 onwards")
    conflicts(
        '+amd-fast-planner',
        when='precision=quad',
        msg="amd-fast-planner doesn't support quad precision")
    conflicts(
        '+amd-fast-planner',
        when='precision=long_double',
        msg="amd-fast-planner doesn't support long_double precision")

    def configure(self, spec, prefix):
        """Configure function"""
        # Base options
        options = [
            '--prefix={0}'.format(prefix),
            '--enable-amd-opt'
        ]

        # Check if compiler is AOCC
        if '%aocc' in spec:
            options.append("CC={0}".format(os.path.basename(spack_cc)))
            options.append("FC={0}".format(os.path.basename(spack_fc)))
            options.append("F77={0}".format(os.path.basename(spack_fc)))

        if '+shared' in spec:
            options.append('--enable-shared')
        else:
            options.append('--disable-shared')

        if '+debug' in spec:
            options.append('--enable-debug')

        if '+openmp' in spec:
            options.append('--enable-openmp')
        else:
            options.append('--disable-openmp')

        if '+threads' in spec:
            options.append('--enable-threads')
        else:
            options.append('--disable-threads')

        if '+mpi' in spec:
            options.append('--enable-mpi')
            options.append('--enable-amd-mpifft')
        else:
            options.append('--disable-mpi')
            options.append('--disable-amd-mpifft')

        if '+amd-fast-planner' in spec:
            options.append('--enable-amd-fast-planner')
        else:
            options.append('--disable-amd-fast-planner')

        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        # Cross compilation is supported in amd-fftw by making use of target
        # variable to set AMD_ARCH configure option.
        # Spack user can not directly use AMD_ARCH for this purpose but should
        # use target variable to set appropriate -march option in AMD_ARCH.
        arch = spec.architecture
        options.append(
            "AMD_ARCH={0}".format(
                arch.target.optimization_flags(
                    spec.compiler).split("=")[-1]))

        # Specific SIMD support.
        # float and double precisions are supported
        simd_features = ['sse2', 'avx', 'avx2']

        simd_options = []
        for feature in simd_features:
            msg = '--enable-{0}' if feature in spec.target else '--disable-{0}'
            simd_options.append(msg.format(feature))

        # When enabling configure option "--enable-amd-opt", do not use the
        # configure option "--enable-generic-simd128" or
        # "--enable-generic-simd256"

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            'float': ['--enable-float'],
            'double': None,
            'long_double': ['--enable-long-double'],
            'quad': ['--enable-quad-precision']
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable('../configure')
        for precision in self.selected_precisions:

            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            if precision in ('float', 'double'):
                opts += simd_options

            with working_dir(precision, create=True):
                configure(*opts)
