# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdmf3(CMakePackage):
    """XDMF, or eXtensible Data Model and Format (XDMF), is a common data model
       format to exchange scientific data between High Performance Computing
       codes and tools.
    """

    homepage = "http://xdmf.org"
    git      = "https://gitlab.kitware.com/xdmf/xdmf.git"

    # There is no official release of XDMF and development has largely ceased,
    # but the current version, 3.x, is maintained on the master branch.
    version('2019-01-14', commit='8d9c98081d89ac77a132d56bc8bef53581db4078')

    variant('shared', default=True, description='Enable shared libraries')
    variant('mpi', default=True, description='Enable MPI')

    depends_on('libxml2')
    depends_on('boost')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')

    def cmake_args(self):
        """Populate cmake arguments for XDMF."""
        spec = self.spec

        cmake_args = [
            '-DBUILD_SHARED_LIBS=%s' % str('+shared' in spec),
            '-DXDMF_BUILD_UTILS=ON',
            '-DXDMF_WRAP_JAVA=OFF',
            '-DXDMF_WRAP_PYTHON=OFF',
            '-DXDMF_BUILD_TESTING=ON'
        ]

        return cmake_args
