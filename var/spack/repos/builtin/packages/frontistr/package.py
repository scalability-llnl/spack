# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Frontistr(CMakePackage):
    """Open-Source Large-Scale Parallel FEM Program for
        Nonlinear Structural Analysis"""

    homepage = "https://www.frontistr.com/"
    git      = "https://gitlab.com/FrontISTR-Commons/FrontISTR.git"
    maintainers = ['hiroshi.okuda', 'kgoto', 'morita', 'inagaki', 'michioga']

    version('5.1.1', tag='v5.1.1')
    version('5.1', tag='v5.1')
    version('5.0', tag='v5.0')
    version('master', tag='master')

    variant('build_type', default='RELEASE',
            description='CMake build type',
            values=('DEBUG', 'RELEASE'))

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('revocap-refiner')
    # depends_on('revocap-coupler')
    depends_on('metis')
    depends_on('mumps')
    depends_on('trilinos@:12.18.1')

    def cmake_args(self):
        define = CMakePackage.define
        cmake_args = [
            define('WITH_ML', True),
        ]
        return cmake_args
