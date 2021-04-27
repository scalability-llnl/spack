# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Gmsh(CMakePackage):
    """Gmsh is a free 3D finite element grid generator with a built-in CAD engine
    and post-processor. Its design goal is to provide a fast, light and
    user-friendly meshing tool with parametric input and advanced visualization
    capabilities. Gmsh is built around four modules: geometry, mesh, solver and
    post-processing. The specification of any input to these modules is done
    either interactively using the graphical user interface or in ASCII text
    files using Gmsh's own scripting language.
    """

    homepage = 'http://gmsh.info'
    url = 'http://gmsh.info/src/gmsh-4.4.1-source.tgz'

    version('4.7.1', sha256='c984c295116c757ed165d77149bd5fdd1068cbd7835e9bcd077358b503891c6a')
    version('4.7.0', sha256='e27f32f92b374ba2a746a9d9c496401c13f66ac6e3e70753e16fa4012d14320e')
    version('4.6.0', sha256='0f2c55e50fb6c478ebc8977f6341c223754cbf3493b7b0d683b4395ae9f2ad1c')
    version('4.5.6', sha256='46eaeb0cdee5822fdaa4b15f92d8d160a8cc90c4565593cfa705de90df2a463f')
    version('4.5.5', sha256='899d3cded664124fa387da57b6f170f47a7e712c7744aa3562779897e2b9e251')
    version('4.5.4', sha256='ccf8c74f43cbe3c371abe79862025d41642b3538a0148f018949494e3b3e2ecd')
    version('4.4.1', sha256='853c6438fc4e4b765206e66a514b09182c56377bb4b73f1d0d26eda7eb8af0dc')
    version('4.2.2', sha256='e9ee9f5c606bbec5f2adbb8c3d6023c4e2577f487fa4e4ecfcfc94a241cc8dcc')
    version('4.0.0',  sha256='fb0c8afa37425c6f4315ab3b3124e9e102fcf270a35198423a4002796f04155f')
    version('3.0.6',  sha256='9700bcc440d7a6b16a49cbfcdcdc31db33efe60e1f5113774316b6fa4186987b')
    version('3.0.1',  sha256='830b5400d9f1aeca79c3745c5c9fdaa2900cdb2fa319b664a5d26f7e615c749f')
    version('2.16.0', sha256='e829eaf32ea02350a385202cc749341f2a3217c464719384b18f653edd028eea')
    version('2.15.0', sha256='992a4b580454105f719f5bc05441d3d392ab0b4b80d4ea07b61ca3bdc974070a')
    version('2.12.0', sha256='7fbd2ec8071e79725266e72744d21e902d4fe6fa9e7c52340ad5f4be5c159d09')
    version('develop', branch='master', git='https://gitlab.onelab.info/gmsh/gmsh.git')

    variant('shared',      default=True,  description='Enables the build of shared libraries')
    variant('mpi',         default=True,  description='Builds MPI support for parser and solver')
    variant('openmp',      default=False, description='Enable OpenMP support')
    variant('fltk',        default=False, description='Enables the build of the FLTK GUI')
    variant('hdf5',        default=False, description='Enables HDF5 support')
    variant('compression', default=True,  description='Enables IO compression through zlib')
    variant('netgen',      default=False, description='Build with Netgen')
    variant('opencascade', default=False, description='Build with OpenCASCADE')
    variant('oce',         default=False, description='Build with OCE')
    variant('petsc',       default=False, description='Build with PETSc')
    variant('slepc',       default=False, description='Build with SLEPc (only when PETSc is enabled)')
    variant('tetgen',      default=False, description='Build with Tetgen')
    variant('metis',       default=False, description='Build with Metis')
    variant('privateapi',  default=False, description='Enable the private API')

    depends_on('blas')
    depends_on('lapack')
    depends_on('cmake@2.8:', type='build')
    depends_on('gmp')
    depends_on('mpi',  when='+mpi')
    # Assumes OpenGL with GLU is already provided by the system:
    depends_on('fltk', when='+fltk')
    depends_on('hdf5', when='+hdf5')
    depends_on('netgen', when='+netgen')
    depends_on('opencascade', when='+opencascade')
    depends_on('oce',  when='+oce')
    depends_on('petsc+mpi', when='+petsc+mpi')
    depends_on('petsc', when='+petsc~mpi')
    depends_on('slepc', when='+slepc+petsc')
    depends_on('tetgen', when='+tetgen')
    depends_on('zlib',  when='+compression')
    depends_on('metis', when='+metis')

    conflicts('+slepc', when='~petsc')
    conflicts('+oce', when='+opencascade')

    def cmake_args(self):
        spec = self.spec
        prefix = self.prefix

        options = []

        # Make sure native file dialogs are used
        options.extend(['-DENABLE_NATIVE_FILE_CHOOSER=ON'])

        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        # Prevent GMsh from using its own strange directory structure on OSX
        options.append('-DENABLE_OS_SPECIFIC_INSTALL=OFF')

        # Make sure GMSH picks up correct BlasLapack by providing linker flags
        blas_lapack = spec['lapack'].libs + spec['blas'].libs
        options.append(
            '-DBLAS_LAPACK_LIBRARIES={0}'.format(blas_lapack.ld_flags))

        # Gmsh does not have an option to compile against external metis.
        # Its own Metis, however, fails to build.
        # However, Metis is needed for the Hxt library.
        if '+metis' in spec:
            options.append('-DENABLE_METIS=ON')
        else:
            options.append('-DENABLE_METIS=OFF')

        if '+fltk' in spec:
            options.append('-DENABLE_FLTK=ON')
        else:
            options.append('-DENABLE_FLTK=OFF')

        if '+oce' in spec:
            env['CASROOT'] = self.spec['oce'].prefix
            options.append('-DENABLE_OCC=ON')
        elif '+opencascade' in spec:
            env['CASROOT'] = self.spec['opencascade'].prefix
            options.append('-DENABLE_OCC=ON')
        else:
            options.append('-DENABLE_OCC=OFF')

        if '+petsc' in spec:
            env['PETSC_DIR'] = self.spec['petsc'].prefix
            options.append('-DENABLE_PETSC=ON')
        else:
            options.append('-DENABLE_PETSC=OFF')

        if '+tetgen' in spec:
            env['TETGEN_DIR'] = self.spec['tetgen'].prefix
            options.append('-DENABLE_TETGEN=ON')
        else:
            options.append('-DENABLE_TETGEN=OFF')

        if '+netgen' in spec:
            env['NETGEN_DIR'] = self.spec['netgen'].prefix
            options.append('-DENABLE_NETGEN=ON')
        else:
            options.append('-DENABLE_NETGEN=OFF')

        if '+slepc' in spec:
            env['SLEPC_DIR'] = self.spec['slepc'].prefix
            options.append('-DENABLE_SLEPC=ON')
        else:
            options.append('-DENABLE_SLEPC=OFF')

        if '+shared' in spec:
            # Builds dynamic executable and installs shared library
            options.extend(['-DENABLE_BUILD_SHARED:BOOL=ON',
                            '-DENABLE_BUILD_DYNAMIC:BOOL=ON'])
        else:
            # Builds and installs static library
            options.append('-DENABLE_BUILD_LIB:BOOL=ON')

        if '+openmp' in spec:
            options.append('-DENABLE_OPENMP=ON')
        else:
            options.append('-DENABLE_OPENMP=OFF')

        if '+mpi' in spec:
            options.append('-DENABLE_MPI:BOOL=ON')

        if '+compression' in spec:
            options.append('-DENABLE_COMPRESSED_IO:BOOL=ON')

        if '+privateapi' in spec:
            options.append('-DENABLE_PRIVATE_API=ON')
        else:
            options.append('-DENABLE_PRIVATE_API=OFF')

        return options
