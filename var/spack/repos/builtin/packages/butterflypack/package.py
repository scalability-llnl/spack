# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Butterflypack(CMakePackage):
    """ButterflyPACK is a mathematical software for rapidly solving
    large-scale dense linear systems that exhibit off-diagonal rank-deficiency.
    These systems arise frequently from boundary element methods, or
    factorization phases in finite-difference/finite-element methods.
    ButterflyPACK relies on low-rank or butterfly formats under Hierarchical
    matrix, HODLR or other hierarchically nested frameworks to compress,
    factor and solve the linear system in quasi-linear time. The
    computationally most intensive phase, factorization, is accelerated via
    randomized linear algebras. The butterfly format, originally inspired by
    the butterfly data flow in fast Fourier Transform, is a linear algebra tool
    well-suited for compressing matrices arising from high-frequency wave
    equations or highly oscillatory integral operators."""

    homepage = "https://github.com/liuyangzhuan/ButterflyPACK"
    git      = "https://github.com/liuyangzhuan/ButterflyPACK.git"
    url      = "https://github.com/liuyangzhuan/ButterflyPACK/archive/v1.0.0.tar.gz"
    maintainers = ['liuyangzhuan']

    version('master', branch='master')
    version('1.0.0', sha256='86c5eb09a18522367d63ce2bacf67ca1c9813ef351a1443baaab3c53f0d77232')
<<<<<<< HEAD
    version('1.0.1', sha256='e8ada37466a19f49e13456b150700d4c3afaad2ddbe3678f4e933f9d556a24a5')
=======

>>>>>>> d480dc53e49bb2b5408eff2ec22699a054e26c4d
    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('arpack-ng')

    def cmake_args(self):
        spec = self.spec

        def on_off(varstr):
            return 'ON' if varstr in spec else 'OFF'

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
            libs.joined(";"),
            '-DTPL_ARPACK_LIBRARIES=%s' % spec['arpack-ng'].libs.joined(";"),
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared'),
        ]

<<<<<<< HEAD

=======
>>>>>>> d480dc53e49bb2b5408eff2ec22699a054e26c4d
        return args
