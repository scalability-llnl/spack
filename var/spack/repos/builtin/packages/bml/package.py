# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bml(CMakePackage):
    """The basic matrix library (bml) is a collection of various matrix data
    formats (in dense and sparse) and their associated algorithms for basic
    matrix operations."""

    homepage = "http://lanl.github.io/bml/"
    url      = "https://github.com/lanl/bml/tarball/v1.2.2"
    git      = "https://github.com/lanl/bml.git"

    version('develop', branch='master')
    version('1.3.1', sha256='17145eda96aa5e550dcbff1ee7ce62b45723af8210b1ab70c5975ec792fa3d13')
    version('1.3.0', sha256='d9465079fe77210eb2af2dcf8ed96802edf5bb76bfbfdbcc97e206c8cd460b07')
    version('1.2.3', sha256='9a2ee6c47d2445bfdb34495497ea338a047e9e4767802af47614d9ff94b0c523')
    version('1.2.2', sha256='89ab78f9fe8395fe019cc0495a1d7b69875b5708069faeb831ddb9a6a9280a8a')
    version('1.1.0', sha256='29162f1f7355ad28b44d3358206ccd3c7ac7794ee13788483abcbd2f8063e7fc')

    variant('shared', default=True, description='Build shared libs')
    variant('mpi', default=True, description='Build with MPI Support')

    conflicts('+mpi', when='@:1.2.2')

    depends_on("blas")
    depends_on("lapack")
    depends_on('mpi', when='+mpi')
    depends_on('python', type='build')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF')
        ]
        spec = self.spec
        if '+mpi' in spec:
            args.append('-DBML_MPI=True')
            args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
            args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        else:
            args.append('-DBML_MPI=False')
        return args
