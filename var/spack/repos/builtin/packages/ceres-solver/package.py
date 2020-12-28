# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CeresSolver(CMakePackage):
    """Ceres Solver is an open source C++ library for modeling and solving
    large, complicated optimization problems. It can be used to solve
    Non-linear Least Squares problems with bounds constraints and general
    unconstrained optimization problems. It is a mature, feature rich, and
    performant library that has been used in production at Google since 2010.
    """

    homepage = "http://ceres-solver.org"
    url      = "http://ceres-solver.org/ceres-solver-1.12.0.tar.gz"

    version('1.14.0', sha256='4744005fc3b902fed886ea418df70690caa8e2ff6b5a90f3dd88a3d291ef8e8e')
    version('1.12.0', sha256='745bfed55111e086954126b748eb9efe20e30be5b825c6dec3c525cf20afc895')

    variant('suitesparse', default=False, description='Build with SuiteSparse')
    variant('shared', default=True, description='Build shared libraries')
    variant('examples', default=False, description='Build examples')

    depends_on('eigen@3:')
    depends_on('lapack')
    depends_on('glog')

    def cmake_args(self):
        args = [
            '-DCXSPARSE=OFF',
            '-DEIGENSPARSE=ON',
            '-DLAPACK=ON',
            '-DSCHUR_SPECIALIZATIONS=OFF'
        ]

        if '+suitesparse' in self.spec:
            args.append('-DSUITESPARSE=ON')
        else:
            args.append('-DSUITESPARSE=OFF')

        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        if '+examples' in self.spec:
            args.append('-DBUILD_EXAMPLES=ON')
        else:
            args.append('-DBUILD_EXAMPLES=OFF')

        return args
