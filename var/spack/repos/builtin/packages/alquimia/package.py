# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alquimia(CMakePackage):
    """Alquimia is an interface that exposes the capabilities
    of mature geochemistry codes such as CrunchFlow and PFLOTRAN"""

    homepage = "https://github.com/LBL-EESA/alquimia-dev"
    git      = "https://github.com/LBL-EESA/alquimia-dev.git"

    maintainers = ['smolins', 'balay']

    version('develop')
    version('xsdk-0.6.0', commit='9a0aedd3a927d4d5e837f8fd18b74ad5a78c3821')
    version('xsdk-0.5.0', commit='8397c3b00a09534c5473ff3ab21f0e32bb159380')
    version('xsdk-0.4.0', commit='2edad6733106142d014bb6e6a73c2b21d5e3cf2d')
    version('xsdk-0.3.0', tag='xsdk-0.3.0')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    depends_on('mpi')
    depends_on('hdf5')
    depends_on('pflotran@xsdk-0.6.0', when='@xsdk-0.6.0')
    depends_on('pflotran@xsdk-0.5.0', when='@xsdk-0.5.0')
    depends_on('pflotran@xsdk-0.4.0', when='@xsdk-0.4.0')
    depends_on('pflotran@xsdk-0.3.0', when='@xsdk-0.3.0')
    depends_on('pflotran@xsdk-0.2.0', when='@xsdk-0.2.0')
    depends_on('pflotran@develop', when='@develop')
    depends_on('petsc@3.10.0:3.10.99', when='@xsdk-0.4.0')
    depends_on('petsc@3.8.0:3.8.99', when='@xsdk-0.3.0')
    depends_on('petsc@xsdk-0.2.0', when='@xsdk-0.2.0')
    depends_on('petsc@3.10:', when='@develop')

    def cmake_args(self):
        spec = self.spec

        options = ['-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                   '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                   '-DUSE_XSDK_DEFAULTS=YES',
                   '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                       'ON' if '+shared' in spec else 'OFF'),
                   '-DTPL_ENABLE_MPI:BOOL=ON',
                   '-DMPI_BASE_DIR:PATH=%s' % spec['mpi'].prefix,
                   '-DTPL_ENABLE_HDF5:BOOL=ON',
                   '-DXSDK_WITH_PFLOTRAN:BOOL=ON',
                   # This is not good.
                   # It assumes that the .a file exists and is not a .so
                   '-DTPL_PFLOTRAN_LIBRARIES=%s' % (
                       spec['pflotran'].prefix.lib + "/libpflotranchem.a"),
                   '-DTPL_PFLOTRAN_INCLUDE_DIRS=%s' % (
                       spec['pflotran'].prefix.include),
                   '-DTPL_ENABLE_PETSC:BOOL=ON',
                   '-DPETSC_EXECUTABLE_RUNS=ON',
                   '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % self.prefix]
        return options
