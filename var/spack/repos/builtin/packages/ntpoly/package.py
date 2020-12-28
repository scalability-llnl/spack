# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ntpoly(CMakePackage):
    """NTPoly - parallel library for computing matrix functions.

    NTPoly is a library for computing the functions of
    sparse, hermitian matrices based on polynomial expansions. For
    sufficiently sparse matrices, most of the matrix functions in
    NTPoly can be computed in linear time.
    """

    homepage = "https://william-dawson.github.io/NTPoly/"
    url      = "https://github.com/william-dawson/NTPoly/archive/ntpoly-v2.3.1.tar.gz"

    version('2.3.1', sha256='af8c7690321607fbdee9671b9cb3acbed945148014e0541435858cf82bfd887e')

    depends_on('cmake', type='build')
    depends_on('blas', type='link')
    depends_on('mpi@3')

    def cmake_args(self):
        args = ["-DNOSWIG=Yes"]
        if self.spec.satisfies('%fj'):
            args.append('-DCMAKE_Fortran_MODDIR_FLAG=-M')

        return args
