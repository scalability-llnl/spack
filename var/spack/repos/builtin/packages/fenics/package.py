##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Fenics(Package):
    """FEniCS is organized as a collection of interoperable components
    that together form the FEniCS Project. These components include
    the problem-solving environment DOLFIN, the form compiler FFC, the
    finite element tabulator FIAT, the just-in-time compiler Instant,
    the code generation interface UFC, the form language UFL and a
    range of additional components."""

    homepage = "http://fenicsproject.org/"
    url      = "https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-1.6.0.tar.gz"

    base_url = "https://bitbucket.org/fenics-project/{pkg}/downloads/{pkg}-{version}.tar.gz"  # NOQA: ignore E501

    variant('hdf5',         default=True,  description='Compile with HDF5')
    variant('parmetis',     default=True,  description='Compile with ParMETIS')
    variant('scotch',       default=True,  description='Compile with Scotch')
    variant('petsc',        default=True,  description='Compile with PETSc')
    variant('slepc',        default=True,  description='Compile with SLEPc')
    variant('trilinos',     default=True,  description='Compile with Trilinos')
    variant('suite-sparse', default=True,  description='Compile with SuiteSparse solvers')
    variant('vtk',          default=False, description='Compile with VTK')
    variant('qt',           default=False, description='Compile with QT')
    variant('mpi',          default=True,  description='Enables the distributed memory support')
    variant('openmp',       default=True,  description='Enables the shared memory support')
    variant('shared',       default=True,  description='Enables the build of shared libraries')
    variant('debug',        default=False, description='Builds a debug version of the libraries')

    # not part of spack list for now
    # variant('petsc4py',     default=True,  description='Uses PETSc4py')
    # variant('slepc4py',     default=True,  description='Uses SLEPc4py')
    # variant('pastix',       default=True,  description='Compile with Pastix')

    extends('python')

    depends_on('py-numpy')
    depends_on('py-ply')
    depends_on('py-six')
    depends_on('py-sphinx@1.0.1:', when='+doc')
    depends_on('eigen@3.2.0:')
    depends_on('boost')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('parmetis@4.0.2:^metis+real64', when='+parmetis')
    depends_on('scotch~metis', when='+scotch~mpi')
    depends_on('scotch+mpi~metis', when='+scotch+mpi')
    depends_on('petsc@3.4:', when='+petsc')
    depends_on('slepc@3.4:', when='+slepc')
    depends_on('trilinos', when='+trilinos')
    depends_on('vtk', when='+vtk')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('qt', when='+qt')

    # This are the build dependencies
    depends_on('py-setuptools')
    depends_on('cmake@2.8.12:')
    depends_on('swig@3.0.3:')

    releases = [
        {
            'version': '1.6.0',
            'md5': '35cb4baf7ab4152a40fb7310b34d5800',
            'resources': {
                'ffc': '358faa3e9da62a1b1a717070217b793e',
                'fiat': 'f4509d05c911fd93cea8d288a78a6c6f',
                'instant': '5f2522eb032a5bebbad6597b6fe0732a',
                'ufl': 'c40c5f04eaa847377ab2323122284016',
            }
        },
        {
            'version': '1.5.0',
            'md5': '9b589a3534299a5e6d22c13c5eb30bb8',
            'resources': {
                'ffc': '343f6d30e7e77d329a400fd8e73e0b63',
                'fiat': 'da3fa4dd8177bb251e7f68ec9c7cf6c5',
                'instant': 'b744023ded27ee9df4a8d8c6698c0d58',
                'ufl': '130d7829cf5a4bd5b52bf6d0955116fd',
            }
        },
    ]

    for release in releases:
        version(release['version'], release['md5'], url=base_url.format(pkg='dolfin', version=release['version']))
        for name, md5 in release['resources'].items():
            resource(name=name,
                     url=base_url.format(pkg=name, **release),
                     md5=md5,
                     destination='depends',
                     when='@{version}'.format(**release),
                     placement=name)

    def cmake_is_on(self, option):
        return 'ON' if option in self.spec else 'OFF'

    def install(self, spec, prefix):
        for package in ['ufl', 'ffc', 'fiat', 'instant']:
            with working_dir(join_path('depends', package)):
                python('setup.py', 'install', '--prefix=%s' % prefix)

        cmake_args = [
            '-DCMAKE_BUILD_TYPE:STRING={0}'.format(
                'Debug' if '+debug' in spec else 'RelWithDebInfo'),
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

        cmake_args.extend(std_cmake_args)

        with working_dir('build', create=True):
            cmake('..', *cmake_args)

            make()
            make('install')
