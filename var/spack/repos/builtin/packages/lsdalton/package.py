# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsdalton(CMakePackage):
    """
    The Dalto nprogram is designed to allow convenient,
    automated determination of a largenumber of molecular properties
    based on an HF, HF-srDFT, DFT, MP2, CC, CI, MCSCF or MC-srDFT
    reference wave function.
    """

    homepage = "https://daltonprogram.org"
    git      = 'https://gitlab.com/dalton/lsdalton.git'

    version('2020.0', tag='v2020.0', submodules=True)

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')

    # gfortran before 9.x won't build due to missing language features support
    # 10.x won't build due to tighter language standards adherence
    conflicts('%gcc@:8')
    conflicts('%gcc@10')

    def cmake_args(self):
        spec = self.spec

        args = ['-DENABLE_BUILTIN_BLAS=OFF',
                '-DENABLE_BUILTIN_LAPACK=OFF',
                '-DUSE_BUILTIN_LAPACK=OFF',
                '-DENABLE_STATIC_LINKING=OFF',
                '-DBUILD_SHARED_LIBS=ON',
                '-DENABLE_MPI=ON',
                '-DUSE_MPIF_H=ON',
                '-DMPIEXEC_MAX_NUMPROCS=128',
                '-DCMAKE_C_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpicc),
                '-DCMAKE_CXX_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpicxx),
                '-DCMAKE_Fortran_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpif90),
                '-DENABLE_PYTHON=OFF',
                '-DENABLE_DEC=ON']

        return args
