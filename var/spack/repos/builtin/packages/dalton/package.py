# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dalton(CMakePackage):
    """
    The Dalto nprogram is designed to allow convenient,
    automated determination of a largenumber of molecular properties
    based on an HF, HF-srDFT, DFT, MP2, CC, CI, MCSCF or MC-srDFT
    reference wave function.
    """

    homepage = "https://daltonprogram.org"
    git      = 'https://gitlab.com/dalton/dalton.git'

    version('2020.0', branch='Dalton2020.0', submodules=True)

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix.join('dalton'))

    def cmake_args(self):
        spec = self.spec

        args = ['-DENABLE_BUILTIN_BLAS=OFF',
                '-DENABLE_BUILTIN_LAPACK=OFF',
                '-DUSE_BUILTIN_LAPACK=OFF',
                '-DENABLE_STATIC_LINKING=OFF',
                '-DENABLE_MPI=ON',
                '-DCMAKE_C_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpicc),
                '-DCMAKE_CXX_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpicxx),
                '-DCMAKE_Fortran_COMPILER={0}'.format(
                    spec['mpi'].prefix.bin.mpif90),
                '-DMPIEXEC_MAX_NUMPROCS=128'
                ]

        return args
