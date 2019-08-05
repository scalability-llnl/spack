# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Visit(CMakePackage):
    """VisIt is an Open Source, interactive, scalable, visualization,
       animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz"

    version('2.13.0', '716644b8e78a00ff82691619d4d1e7a914965b6535884890b667b97ba08d6a0f')
    version('2.12.3', '2dd351a291ee3e79926bc00391ca89b202cfa4751331b0fdee1b960c7922161f')
    version('2.12.2', '355779b1dbf440cdd548526eecd77b60')
    version('2.10.3', 'a1082a6f6dab3e2dcb58993603456c2b')
    version('2.10.2', '253de0837a9d69fb689befc98ea4d068')
    version('2.10.1', '3cbca162fdb0249f17c4456605c4211e')

    variant('gui',    default=True, description='Enable VisIt\'s GUI')
    variant('hdf5',   default=True, description='Enable HDF5 file format')
    variant('silo',   default=True, description='Enable Silo file format')
    variant('python', default=True, description='Enable Python support')
    variant('mpi',    default=True, description='Enable parallel engine')

    depends_on('cmake@3.0:', type='build')
    depends_on('vtk@6.1.0~opengl2~mpi')
    depends_on('qt@4.8.6', when='+gui')
    depends_on('qwt', when='+gui')
    depends_on('python', when='+python')
    depends_on('silo+shared', when='+silo')
    depends_on('hdf5', when='+hdf5')
    depends_on('mpi', when='+mpi')

    patch('parallel-hdf5-name-fix.patch', when='+hdf5 +mpi')
    patch('https://aur.archlinux.org/cgit/aur.git/plain/fix_type.patch?h=visit',
            level=0,
            working_dir='src',
            sha256=('9357fef64b4008a1044a804638ab1e2b'
                    '8ca2faaec0bcc8cd4890fc3469017892'))

    conflicts('+hdf5', when='~gui')
    conflicts('+silo', when='~gui')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DVTK_MAJOR_VERSION={0}'.format(spec['vtk'].version[0]),
            '-DVTK_MINOR_VERSION={0}'.format(spec['vtk'].version[1]),
            '-DVISIT_VTK_DIR:PATH={0}'.format(spec['vtk'].prefix),
            '-DVISIT_USE_GLEW=OFF',
            '-DCMAKE_CXX_FLAGS=-fPIC',
            '-DCMAKE_C_FLAGS=-fPIC'
        ]

        if(spec.variants['python'].value):
            args.append('-DPYTHON_DIR:PATH={0}'.format(spec['python'].home))

        if(spec.variants['gui'].value):
            qt_bin = spec['qt'].prefix.bin
            args.append(
                '-DVISIT_LOC_QMAKE_EXE:FILEPATH={0}/qmake-qt4'.format(qt_bin))
            args.append('-DVISIT_QWT_DIR:PATH={0}'.format(spec['qwt'].prefix))
        else:
            args.append('-DVISIT_SERVER_COMPONENTS_ONLY=ON')
            args.append('-DVISIT_ENGINE_ONLY=ON')

        if(spec.variants['hdf5'].value):
            args.append(
                '-DVISIT_HDF5_DIR:PATH={0}'.format(spec['hdf5'].prefix))
            if spec.satisfies('^hdf5+mpi', strict=True):
                args.append('-DVISIT_HDF5_MPI_DIR:PATH={0}'.format(
                    spec['hdf5'].prefix))

        if(spec.variants['silo'].value):
            args.append(
                '-DVISIT_SILO_DIR:PATH={0}'.format(spec['silo'].prefix))

        if(spec.variants['mpi'].value):
            args.append('-DVISIT_PARALLEL=ON')
            args.append('-DVISIT_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DVISIT_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))
            args.append('-DVISIT_MPI_COMPILER={0}'.format(spec['mpi'].mpicxx))

        return args
