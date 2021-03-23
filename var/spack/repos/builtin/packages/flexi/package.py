# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flexi(CMakePackage):
    """Open Source High-Order Unstructured Discontinuous Galerkin Fluid
    Dynamics Solver"""

    homepage = "https://www.flexi-project.org/"
    git      = "https://github.com/flexi-framework/flexi.git"

    version('master')

    patch('for_aarch64.patch', when='target=aarch64:')

    variant('mpi', default=True, description='Enable MPI')

    depends_on('mpi', when='+mpi')
    depends_on('hdf5+fortran+mpi', when='+mpi')
    depends_on('hdf5+fortran~mpi', when='~mpi')
    depends_on('lapack')
    depends_on('zlib')

    def flag_handler(self, name, flags):
        if name == 'fflags':
            if self.spec.satisfies('%gcc@10:'):
                if flags is None:
                    flags = []
                flags.append('-fallow-argument-mismatch')

        return (flags, None, None)

    def cmake_args(self):
        args = [
            '-DFLEXI_BUILD_HDF5:BOOL=OFF',
            self.define_from_variant('FLEXI_MPI', 'mpi')
        ]

        return args
