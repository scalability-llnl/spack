# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hiop(CMakePackage):
    """HiOp is an optimization solver for solving certain mathematical
    optimization problems expressed as nonlinear programming problems.
    HiOp is a lightweight HPC solver that leverages application's existing
    data parallelism to parallelize the optimization iterations by using
    specialized linear algebra kernels."""

    homepage = "https://github.com/LLNL/hiop"
    git      = "https://github.com/LLNL/hiop.git"

    version('0.1', tag='v0.1')

    variant('mpi', default=True,
            description='Enable/Disable MPI')

    variant('deepchecking', default=True,
            description='Ultra safety checks - \
            used for increased robustness and self-diagnostics')

    depends_on('mpi', when='+mpi')
    depends_on('lapack')
    depends_on('blas')

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        if '+mpi' in spec:
            args.append("-DWITH_MPI=ON")
        else:
            args.append("-DWITH_MPI=OFF")

        if '+deepchecking' in spec:
            args.append("-DDEEP_CHECKING=ON")
        else:
            args.append("-DDEEP_CHECKING=OFF")

        lapack_blas_libs = (
            spec['lapack'].libs + spec['blas'].libs).joined(';')
        args.extend([
            '-DLAPACK_FOUND=TRUE',
            '-DLAPACK_LIBRARIES={0}'.format(lapack_blas_libs)
        ])

        return args
