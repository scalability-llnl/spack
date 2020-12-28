# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Strumpack(CMakePackage, CudaPackage):
    """STRUMPACK -- STRUctured Matrix PACKage - provides linear solvers
    for sparse matrices and for dense rank-structured matrices, i.e.,
    matrices that exhibit some kind of low-rank property. It provides a
    distributed memory fully algebraic sparse solver and
    preconditioner. The preconditioner is mostly aimed at large sparse
    linear systems which result from the discretization of a partial
    differential equation, but is not limited to any particular type of
    problem. STRUMPACK also provides preconditioned GMRES and BiCGStab
    iterative solvers."""

    homepage = "http://portal.nersc.gov/project/sparse/strumpack"
    url      = "https://github.com/pghysels/STRUMPACK/archive/v4.0.0.tar.gz"
    git      = "https://github.com/pghysels/STRUMPACK.git"

    maintainers = ['pghysels']

    version('master', branch='master')
    version('5.0.0', sha256='bdfd1620ff7158d96055059be04ee49466ebaca8213a2fdab33e2d4571019a49')
    version('4.0.0', sha256='a3629f1f139865c74916f8f69318f53af6319e7f8ec54e85c16466fd7d256938')
    version('3.3.0', sha256='499fd3b58656b4b6495496920e5372895861ebf15328be8a7a9354e06c734bc7')
    version('3.2.0', sha256='34d93e1b2a3b8908ef89804b7e08c5a884cbbc0b2c9f139061627c0d2de282c1')
    version('3.1.1', sha256='c1c3446ee023f7b24baa97b24907735e89ce4ae9f5ef516645dfe390165d1778')

    variant('shared', default=False, description='Build shared libraries')
    variant('mpi', default=True, description='Use MPI')
    variant('openmp', default=True,
            description='Enable thread parallellism via tasking with OpenMP')
    variant('cuda', default=True,
            description='Enable CUDA support')
    variant('parmetis', default=True,
            description='Enable use of ParMetis')
    variant('scotch', default=False,
            description='Enable use of Scotch')
    variant('butterflypack', default=True,
            description='Enable use of ButterflyPACK')
    variant('zfp', default=True,
            description='Build with support for compression using ZFP')
    variant('c_interface', default=True,
            description='Enable C interface')
    variant('count_flops', default=False,
            description='Build with flop counters')
    variant('task_timers', default=False,
            description='Build with timers for internal routines')
    variant('build_dev_tests', default=False,
            description='Build developer test routines')
    variant('build_tests', default=False,
            description='Build test routines')

    # TODO: add a slate variant

    depends_on('cmake@3.11:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scotch~metis', when='+scotch')
    depends_on('scotch~metis+mpi', when='+scotch+mpi')
    depends_on('butterflypack@1.1.0', when='@3.3.0:3.9.999 +butterflypack+mpi')
    depends_on('butterflypack@1.2.0:', when='@4.0.0: +butterflypack+mpi')
    depends_on('cuda', when='@4.0.0: +cuda')
    depends_on('zfp', when='+zfp')

    conflicts('+parmetis', when='~mpi')
    conflicts('+butterflypack', when='~mpi')
    conflicts('+butterflypack', when='@:3.2.0')
    conflicts('+cuda', when='@:3.9.999')
    conflicts('+zfp', when='@:3.9.999')

    patch('intel-19-compile.patch', when='@3.1.1')

    def cmake_args(self):
        spec = self.spec

        def on_off(varstr):
            return 'ON' if varstr in spec else 'OFF'

        args = [
            '-DSTRUMPACK_USE_MPI=%s' % on_off('+mpi'),
            '-DSTRUMPACK_USE_OPENMP=%s' % on_off('+openmp'),
            '-DTPL_ENABLE_PARMETIS=%s' % on_off('+parmetis'),
            '-DTPL_ENABLE_SCOTCH=%s' % on_off('+scotch'),
            '-DTPL_ENABLE_BPACK=%s' % on_off('+butterflypack'),
            '-DSTRUMPACK_COUNT_FLOPS=%s' % on_off('+count_flops'),
            '-DSTRUMPACK_TASK_TIMERS=%s' % on_off('+task_timers'),
            '-DSTRUMPACK_DEV_TESTING=%s' % on_off('+build_dev_tests'),
            '-DSTRUMPACK_BUILD_TESTS=%s' % on_off('+build_tests'),
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
            libs.joined(";"),
        ]

        if spec.satisfies('@:3.9.999'):
            if '+mpi' in spec:
                args.extend([
                    '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
                ])
            args.extend([
                '-DSTRUMPACK_C_INTERFACE=%s' % on_off('+c_interface'),
            ])

        if spec.satisfies('@4.0.0:'):
            args.extend([
                '-DSTRUMPACK_USE_CUDA=%s' % on_off('+cuda')
            ])

        args.extend([
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared')
        ])

        return args
