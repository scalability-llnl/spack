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
import sys


class Dealii(Package):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""
    homepage = "https://www.dealii.org"
    url      = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"

    version('8.4.1', 'efbaf16f9ad59cfccad62302f36c3c1d')
    version('8.4.0', 'ac5dbf676096ff61e092ce98c80c2b00')
    version('8.3.0', 'fc6cdcb16309ef4bea338a4f014de6fa')
    version('8.2.1', '71c728dbec14f371297cd405776ccf08')
    version('8.1.0', 'aa8fadc2ce5eb674f44f997461bf668d')
    version('dev', git='https://github.com/dealii/dealii.git')

    variant('mpi',      default=True,  description='Compile with MPI')
    variant('arpack',   default=True,  description='Compile with Arpack and PArpack (only with MPI)')
    variant('doc',      default=False, description='Compile with documentation')
    variant('gsl',      default=True,  description='Compile with GSL')
    variant('hdf5',     default=True,  description='Compile with HDF5 (only with MPI)')
    variant('metis',    default=True,  description='Compile with Metis')
    variant('netcdf',   default=True,  description='Compile with Netcdf (only with MPI)')
    variant('oce',      default=True,  description='Compile with OCE')
    variant('p4est',    default=True,  description='Compile with P4est (only with MPI)')
    variant('petsc',    default=True,  description='Compile with Petsc (only with MPI)')
    variant('slepc',    default=True,  description='Compile with Slepc (only with Petsc and MPI)')
    variant('trilinos', default=True,  description='Compile with Trilinos (only with MPI)')

    # required dependencies, light version
    depends_on("blas")
    # Boost 1.58 is blacklisted, see
    # https://github.com/dealii/dealii/issues/1591
    # Require at least 1.59
    depends_on("boost@1.59.0:+thread+system+serialization+iostreams",     when='~mpi')  # NOQA: ignore=E501
    depends_on("boost@1.59.0:+mpi+thread+system+serialization+iostreams", when='+mpi')  # NOQA: ignore=E501
    depends_on("bzip2")
    depends_on("cmake")
    depends_on("lapack")
    depends_on("muparser")
    depends_on("suite-sparse")
    depends_on("tbb")
    depends_on("zlib")

    # optional dependencies
    depends_on("mpi",              when="+mpi")
    depends_on("arpack-ng+mpi",    when='+arpack+mpi')
    depends_on("doxygen+graphviz", when='+doc')
    depends_on("graphviz",         when='+doc')
    depends_on("gsl",              when='@8.5.0:+gsl')
    depends_on("gsl",              when='@dev+gsl')
    depends_on("hdf5+mpi",         when='+hdf5+mpi')
    depends_on("metis@5:",         when='+metis')
    depends_on("netcdf+mpi",       when="+netcdf+mpi")
    depends_on("netcdf-cxx",       when='+netcdf+mpi')
    depends_on("oce",              when='+oce')
    depends_on("p4est",            when='+p4est+mpi')
    depends_on("petsc@:3.6.4+mpi", when='+petsc+mpi')  # FIXME: update after 3.7 is supported upstream.  # NOQA: ignore=E501
    depends_on("slepc@:3.6.3",     when='+slepc+petsc+mpi')
    depends_on("trilinos",         when='+trilinos+mpi')

    # developer dependnecies
    depends_on("numdiff",     when='@dev')
    depends_on("astyle@2.04", when='@dev')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        # CMAKE_BUILD_TYPE should be DebugRelease | Debug | Release
        for word in options[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                options.remove(word)

        dsuf = 'dylib' if sys.platform == 'darwin' else 'so'
        options.extend([
            '-DCMAKE_BUILD_TYPE=DebugRelease',
            '-DDEAL_II_COMPONENT_EXAMPLES=ON',
            '-DDEAL_II_WITH_THREADS:BOOL=ON',
            '-DBOOST_DIR=%s' % spec['boost'].prefix,
            '-DBZIP2_DIR=%s' % spec['bzip2'].prefix,
            # CMake's FindBlas/Lapack may pickup system's blas/lapack instead
            # of Spack's. Be more specific to avoid this.
            # Note that both lapack and blas are provided in -DLAPACK_XYZ.
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS=%s;%s' % (
                spec['lapack'].prefix.include, spec['blas'].prefix.include),
            '-DLAPACK_LIBRARIES=%s;%s' % (
                spec['lapack'].lapack_shared_lib,
                spec['blas'].blas_shared_lib),
            '-DMUPARSER_DIR=%s' % spec['muparser'].prefix,
            '-DUMFPACK_DIR=%s' % spec['suite-sparse'].prefix,
            '-DTBB_DIR=%s' % spec['tbb'].prefix,
            '-DZLIB_DIR=%s' % spec['zlib'].prefix
        ])

        # MPI
        if '+mpi' in spec:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=ON',
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_MPI:BOOL=OFF',
            ])

        # Optional dependencies for which librariy names are the same as CMake
        # variables:
        for library in ('gsl', 'hdf5', 'p4est', 'petsc', 'slepc', 'trilinos', 'metis'):  # NOQA: ignore=E501
            if library in spec:
                options.extend([
                    '-D%s_DIR=%s' % (library.upper(), spec[library].prefix),
                    '-DDEAL_II_WITH_%s:BOOL=ON' % library.upper()
                ])
            else:
                options.extend([
                    '-DDEAL_II_WITH_%s:BOOL=OFF' % library.upper()
                ])

        # doxygen
        options.extend([
            '-DDEAL_II_COMPONENT_DOCUMENTATION=%s' %
            ('ON' if '+doc' in spec else 'OFF'),
        ])

        # arpack
        if '+arpack' in spec:
            options.extend([
                '-DARPACK_DIR=%s' % spec['arpack-ng'].prefix,
                '-DDEAL_II_WITH_ARPACK=ON',
                '-DDEAL_II_ARPACK_WITH_PARPACK=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_ARPACK=OFF'
            ])

        # since Netcdf is spread among two, need to do it by hand:
        if '+netcdf' in spec:
            options.extend([
                '-DNETCDF_FOUND=true',
                '-DNETCDF_LIBRARIES=%s;%s' % (
                    join_path(spec['netcdf-cxx'].prefix.lib,
                              'libnetcdf_c++.%s' % dsuf),
                    join_path(spec['netcdf'].prefix.lib,
                              'libnetcdf.%s' % dsuf)),
                '-DNETCDF_INCLUDE_DIRS=%s;%s' % (
                    spec['netcdf-cxx'].prefix.include,
                    spec['netcdf'].prefix.include),
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_NETCDF=OFF'
            ])

        # Open Cascade
        if '+oce' in spec:
            options.extend([
                '-DOPENCASCADE_DIR=%s' % spec['oce'].prefix,
                '-DDEAL_II_WITH_OPENCASCADE=ON'
            ])
        else:
            options.extend([
                '-DDEAL_II_WITH_OPENCASCADE=OFF'
            ])

        cmake('.', *options)

        make()
        make("test")
        make("install")

        # run some MPI examples with different solvers from PETSc and Trilinos
        env['DEAL_II_DIR'] = prefix
        print('=====================================')
        print('============ EXAMPLES ===============')
        print('=====================================')
        # take bare-bones step-3
        print('=====================================')
        print('============ Step-3 =================')
        print('=====================================')
        with working_dir('examples/step-3'):
            cmake('.')
            make('release')
            make('run', parallel=False)

        # An example which uses Metis + PETSc
        # FIXME: switch step-18 to MPI
        with working_dir('examples/step-18'):
            print('=====================================')
            print('============= Step-18 ===============')
            print('=====================================')
            # list the number of cycles to speed up
            filter_file(r'(end_time = 10;)',  ('end_time = 3;'), 'step-18.cc')
            if '^petsc' in spec and '^metis' in spec:
                cmake('.')
                make('release')
                make('run', parallel=False)

        # take step-40 which can use both PETSc and Trilinos
        # FIXME: switch step-40 to MPI run
        with working_dir('examples/step-40'):
            print('=====================================')
            print('========== Step-40 PETSc ============')
            print('=====================================')
            # list the number of cycles to speed up
            filter_file(r'(const unsigned int n_cycles = 8;)',
                        ('const unsigned int n_cycles = 2;'), 'step-40.cc')
            cmake('.')
            if '^petsc' in spec:
                make('release')
                make('run', parallel=False)

            print('=====================================')
            print('========= Step-40 Trilinos ==========')
            print('=====================================')
            # change Linear Algebra to Trilinos
            # The below filter_file should be different for versions
            # before and after 8.4.0
            if spec.satisfies('@8.4.0:'):
                filter_file(r'(\/\/ #define FORCE_USE_OF_TRILINOS.*)',
                            ('#define FORCE_USE_OF_TRILINOS'), 'step-40.cc')
            else:
                filter_file(r'(#define USE_PETSC_LA.*)',
                            ('// #define USE_PETSC_LA'), 'step-40.cc')
            if '^trilinos+hypre' in spec:
                make('release')
                make('run', parallel=False)

            # the rest of the tests on step 40 only works for
            # dealii version 8.4.0 and after
            if spec.satisfies('@8.4.0:'):
                print('=====================================')
                print('=== Step-40 Trilinos SuperluDist ====')
                print('=====================================')
                # change to direct solvers
                filter_file(r'(LA::SolverCG solver\(solver_control\);)',  ('TrilinosWrappers::SolverDirect::AdditionalData data(false,"Amesos_Superludist"); TrilinosWrappers::SolverDirect solver(solver_control,data);'), 'step-40.cc')  # NOQA: ignore=E501
                filter_file(r'(LA::MPI::PreconditionAMG preconditioner;)',
                            (''), 'step-40.cc')
                filter_file(r'(LA::MPI::PreconditionAMG::AdditionalData data;)',  # NOQA: ignore=E501
                            (''), 'step-40.cc')
                filter_file(r'(preconditioner.initialize\(system_matrix, data\);)',  # NOQA: ignore=E501
                            (''), 'step-40.cc')
                filter_file(r'(solver\.solve \(system_matrix, completely_distributed_solution, system_rhs,)',  ('solver.solve (system_matrix, completely_distributed_solution, system_rhs);'), 'step-40.cc')  # NOQA: ignore=E501
                filter_file(r'(preconditioner\);)',  (''), 'step-40.cc')
                if '^trilinos+superlu-dist' in spec:
                    make('release')
                    make('run', paralle=False)

                print('=====================================')
                print('====== Step-40 Trilinos MUMPS =======')
                print('=====================================')
                # switch to Mumps
                filter_file(r'(Amesos_Superludist)',
                            ('Amesos_Mumps'), 'step-40.cc')
                if '^trilinos+mumps' in spec:
                    make('release')
                    make('run', parallel=False)

        print('=====================================')
        print('============ Step-36 ================')
        print('=====================================')
        with working_dir('examples/step-36'):
            if 'slepc' in spec:
                cmake('.')
                make('release')
                make('run', parallel=False)

        print('=====================================')
        print('============ Step-54 ================')
        print('=====================================')
        with working_dir('examples/step-54'):
            if 'oce' in spec:
                cmake('.')
                make('release')
                make('run', parallel=False)

    def setup_environment(self, spack_env, env):
        env.set('DEAL_II_DIR', self.prefix)
