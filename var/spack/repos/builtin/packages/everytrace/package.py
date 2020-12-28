# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Everytrace(CMakePackage):
    """Get stack trace EVERY time a program exits."""

    homepage = "https://github.com/citibeth/everytrace"
    url      = "https://github.com/citibeth/everytrace/archive/0.2.2.tar.gz"
    git      = "https://github.com/citibeth/everytrace.git"

    maintainers = ['citibeth']

    version('develop', branch='develop')
    version('0.2.2', sha256='0487276bb24e648388862d8e1d8cfe56b529f7e3d840df3fcb5b3a3dad4016e1')

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('fortran', default=True,
            description='Enable use with Fortran programs')
    variant('cxx', default=True, description='Enable C++ Exception-based features')

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_FORTRAN=%s' % ('YES' if '+fortran' in spec else 'NO'),
            '-DUSE_CXX=%s' % ('YES' if '+cxx' in spec else 'NO')]
