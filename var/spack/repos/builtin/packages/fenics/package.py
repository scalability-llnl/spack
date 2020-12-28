# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fenics(CMakePackage):
    """FEniCS is organized as a collection of interoperable components
    that together form the FEniCS Project. These components include
    the problem-solving environment DOLFIN, the form compiler FFC, the
    finite element tabulator FIAT, the just-in-time compiler Instant,
    the code generation interface UFC, the form language UFL and a
    range of additional components."""

    homepage = "http://fenicsproject.org/"
    url      = "https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-1.6.0.tar.gz"
    base_url = "https://bitbucket.org/fenics-project/{pkg}/downloads/{pkg}-{version}.tar.gz"

    python_components = ['ufl', 'ffc', 'fiat', 'instant']

    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('parmetis',     default=True,  description='Compile with ParMETIS')
    variant('scotch',       default=True,  description='Compile with Scotch')
    variant('petsc',        default=True,  description='Compile with PETSc')
    variant('slepc',        default=True,  description='Compile with SLEPc')
    variant('trilinos',     default=True,  description='Compile with Trilinos')
    variant('suite-sparse', default=True,
            description='Compile with SuiteSparse solvers')
    variant('vtk',          default=False, description='Compile with VTK')
    variant('qt',           default=False, description='Compile with QT')
    variant('mpi',          default=True,
            description='Enables the distributed memory support')
    variant('openmp',       default=True,
            description='Enables the shared memory support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('doc',          default=False,
            description='Builds the documentation')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Developer'))

    # not part of spack list for now
    # variant('petsc4py',     default=True,  description='Uses PETSc4py')
    # variant('slepc4py',     default=True,  description='Uses SLEPc4py')
    # variant('pastix',       default=True,  description='Compile with Pastix')

    patch('petsc-3.7.patch', when='@1.6.1^petsc@3.7:')
    patch('petsc-version-detection.patch', when='@:1.6.1')
    patch('hdf5~cxx-detection.patch')

    extends('python')

    depends_on('eigen@3.2.0:')
    depends_on('boost+filesystem+program_options+system+iostreams+timer+regex+chrono')

    depends_on('mpi', when='+mpi')
    # FIXME: next line fixes concretization with petsc
    depends_on('hdf5+hl+fortran', when='+hdf5+petsc')
    depends_on('hdf5+hl', when='+hdf5~petsc')
    depends_on('parmetis@4.0.2:', when='+parmetis')
    depends_on('metis+real64', when='+parmetis')
    depends_on('scotch~metis', when='+scotch~mpi')
    depends_on('scotch+mpi~metis', when='+scotch+mpi')
    depends_on('petsc@3.4:', when='+petsc')
    depends_on('slepc@3.4:', when='+slepc')
    depends_on('trilinos', when='+trilinos')
    depends_on('vtk', when='+vtk')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('qt', when='+qt')

    depends_on('py-ply', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))
    depends_on('swig@3.0.3:', type=('build', 'run'))
    depends_on('cmake@2.8.12:', type='build')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@1.0.1:', when='+doc', type='build')

    releases = [
        {
            'version': '2016.1.0',
            'sha256': '6228b4d641829a4cd32141bfcd217a1596a27d5969aa00ee64ebba2b1c0fb148',
            'resources': {
                'ffc': '52430ce4c7d57ce1b81eb5fb304992247c944bc6a6054c8b6f42bac81702578d',
                'fiat': '851723126a71bc1ae2dc4ad6e9330bd9b54d52db390dcbbc1f3c759fb49c6aeb',
                'instant': '7bf03c8a7b61fd1e432b8f3a0405410ae68892ebb1a62a9f8118e8846bbeb0c6',
                'ufl': '8dccfe10d1251ba48a4d43a4c6c89abe076390223b500f4baf06f696294b8dd0',
            }
        },
        {
            'version': '1.6.0',
            'sha256': '67eaac5fece6e71da0559b4ca8423156f9e99a952f0620adae449ebebb6695d1',
            'resources': {
                'ffc': '382e7713fe759694e5f07506b144eeead681e169e5a34c164ef3da30eddcc1c6',
                'fiat': '858ea3e936ad3b3558b474ffccae8a7b9dddbaafeac77e307115b23753cb1cac',
                'instant': '2347e0229531969095911fdb1de30bd77bdd7f81521ba84d81b1b4a564fc906c',
                'ufl': 'c75c4781e5104504f158cb42cd87aceffa9052e8e9db6e9764e6a5b6115d7f73',
            }
        },
    ]

    for release in releases:
        version(release['version'], release['sha256'], url=base_url.format(
            pkg='dolfin', version=release['version']))
        for rname, sha256 in release['resources'].items():
            resource(name=rname,
                     url=base_url.format(pkg=rname, **release),
                     sha256=sha256,
                     destination='depends',
                     when='@{version}'.format(**release),
                     placement=rname)

    def cmake_is_on(self, option):
        return 'ON' if option in self.spec else 'OFF'

    def cmake_args(self):
        return [
            '-DDOLFIN_ENABLE_DOCS:BOOL={0}'.format(
                self.cmake_is_on('+doc')),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                self.cmake_is_on('+shared')),
            '-DDOLFIN_SKIP_BUILD_TESTS:BOOL=ON',
            '-DDOLFIN_ENABLE_OPENMP:BOOL={0}'.format(
                self.cmake_is_on('+openmp')),
            '-DDOLFIN_ENABLE_CHOLMOD:BOOL={0}'.format(
                self.cmake_is_on('suite-sparse')),
            '-DDOLFIN_ENABLE_HDF5:BOOL={0}'.format(
                self.cmake_is_on('hdf5')),
            '-DDOLFIN_ENABLE_MPI:BOOL={0}'.format(
                self.cmake_is_on('mpi')),
            '-DDOLFIN_ENABLE_PARMETIS:BOOL={0}'.format(
                self.cmake_is_on('parmetis')),
            '-DDOLFIN_ENABLE_PASTIX:BOOL={0}'.format(
                self.cmake_is_on('pastix')),
            '-DDOLFIN_ENABLE_PETSC:BOOL={0}'.format(
                self.cmake_is_on('petsc')),
            '-DDOLFIN_ENABLE_PETSC4PY:BOOL={0}'.format(
                self.cmake_is_on('py-petsc4py')),
            '-DDOLFIN_ENABLE_PYTHON:BOOL={0}'.format(
                self.cmake_is_on('python')),
            '-DDOLFIN_ENABLE_QT:BOOL={0}'.format(
                self.cmake_is_on('qt')),
            '-DDOLFIN_ENABLE_SCOTCH:BOOL={0}'.format(
                self.cmake_is_on('scotch')),
            '-DDOLFIN_ENABLE_SLEPC:BOOL={0}'.format(
                self.cmake_is_on('slepc')),
            '-DDOLFIN_ENABLE_SLEPC4PY:BOOL={0}'.format(
                self.cmake_is_on('py-slepc4py')),
            '-DDOLFIN_ENABLE_SPHINX:BOOL={0}'.format(
                self.cmake_is_on('py-sphinx')),
            '-DDOLFIN_ENABLE_TRILINOS:BOOL={0}'.format(
                self.cmake_is_on('trilinos')),
            '-DDOLFIN_ENABLE_UMFPACK:BOOL={0}'.format(
                self.cmake_is_on('suite-sparse')),
            '-DDOLFIN_ENABLE_VTK:BOOL={0}'.format(
                self.cmake_is_on('vtk')),
            '-DDOLFIN_ENABLE_ZLIB:BOOL={0}'.format(
                self.cmake_is_on('zlib')),
        ]

    @run_after('build')
    def build_python_components(self):
        for package in self.python_components:
            with working_dir(join_path('depends', package)):
                setup_py('build')

    @run_after('install')
    def install_python_components(self):
        for package in self.python_components:
            with working_dir(join_path('depends', package)):
                setup_py('install', '--prefix={0}'.format(self.prefix))
