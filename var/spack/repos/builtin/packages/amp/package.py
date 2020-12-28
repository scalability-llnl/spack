# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amp(CMakePackage):
    """The Advanced Multi-Physics (AMP) package is an open source parallel
    object-oriented computational framework that is designed with single
    and multi-domain multi-physics applications in mind. AMP can be used
    to build powerful and flexible multi-physics simulation algorithms
    from lightweight operator, solver, linear algebra, material database,
    discretization, and meshing components. The AMP design is meant to
    enable existing investments in application codes to be leveraged without
    having to adopt dramatically different data structures while developing
    new computational science applications. Application components are
    represented as discrete mathematical operators that only require a
    minimal interface and through operator composition the incremental
    development of complex parallel applications is enabled. AMP is meant
    to allow application domain scientists, computer scientists and
    mathematicians to simulate, collaborate, and conduct research on
    various aspects of massively parallel simulation algorithms."""

    homepage = "https://bitbucket.org/AdvancedMultiPhysics/amp"
    hg       = homepage

    version('develop')

    # Everything should be compiled position independent (-fpic)
    depends_on('blas')
    depends_on('lapack')
    depends_on('boost', when='+boost')
    depends_on('petsc', when='+petsc')
    depends_on('trilinos', when='+trilinos')
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5', when='+silo')
    depends_on('silo', when='+silo')
    depends_on('zlib', when="+zlib")

    # MPI related dependencies
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        spec = self.spec

        options = []

        # #################### Base Settings #######################

        options.extend([
            '-DTPL_URL=https://bitbucket.org/AdvancedMultiPhysics/tpl-builder',
            '-DAMP_DATA_URL=https://bitbucket.org/AdvancedMultiPhysics/amp/downloads/AMP-Data.tar.gz',
            '-DAMP_ENABLE_TESTS:BOOL=OFF',
            '-DAMP_ENABLE_EXAMPLES:BOOL=OFF',
            '-DAMP_ENABLE_CXX11:BOOL=ON',
            '-DCXX_STD=11',
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
        ])

        # #################### Compiler Settings #######################

        if '+mpi' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DUSE_MPI=0',
                '-DMPI_COMPILER=1',
                '-DMPIEXEC=$s'                % spec['mpi'].prefix.bin,
            ])
        else:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % self.compiler.cc,
                '-DCMAKE_CXX_COMPILER=%s'     % self.compiler.cxx,
                '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.fc,
                '-DUSE_MPI=0',
            ])

        # ################## Third Party Libraries #####################

        tpl_list = "LAPACK"
        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        options.extend([
            '-DTPL_LAPACK_INSTALL_DIR=%s' % spec['lapack'].prefix,
            '-DTPL_BLAS_LIBRARY_NAMES=%s' % ';'.join(blas.names),
            '-DTPL_BLAS_LIBRARY_DIRS=%s' % ';'.join(blas.directories),
            '-DTPL_LAPACK_LIBRARY_NAMES=%s' % ';'.join(lapack.names),
            '-DTPL_LAPACK_LIBRARY_DIRS=%s' % ';'.join(lapack.directories),
        ])
        if '+boost' in spec:
            tpl_list = tpl_list + ";BOOST"
            options.extend(['-DTPL_BOOST_INSTALL_DIR=%s' %
                            spec['boost'].prefix, ])
        if '+zlib' in spec:
            tpl_list = tpl_list + ";ZLIB"
            options.extend(['-DTPL_ZLIB_INSTALL_DIR=%s' %
                            spec['zlib'].prefix, ])
        if '+hdf5' in spec:
            tpl_list = tpl_list + ";HDF5"
            options.extend(['-DTPL_HDF5_INSTALL_DIR=%s' %
                            spec['hdf5'].prefix, ])
        if '+silo' in spec:
            tpl_list = tpl_list + ";SILO"
            options.extend(['-DTPL_SILO_INSTALL_DIR=%s' %
                            spec['silo'].prefix, ])
        if '+netcdf' in spec:
            tpl_list = tpl_list + ";NETCDF"
            options.extend(['-DTPL_NETCDF_INSTALL_DIR=%s' %
                            spec['netcdf-c'].prefix, ])
        if '+hypre' in spec:
            tpl_list = tpl_list + ";HYPRE"
            options.extend(['-DTPL_HYPRE_INSTALL_DIR=%s' %
                            spec['hypre'].prefix, ])
        if '+petsc' in spec:
            tpl_list = tpl_list + ";PETSC"
            options.extend(['-DTPL_PETSC_INSTALL_DIR=%s' %
                            spec['petsc'].prefix, ])
        if '+trilinos' in spec:
            tpl_list = tpl_list + ";TRILINOS"
            options.extend(['-DTPL_TRILINOS_INSTALL_DIR=%s' %
                            spec['trilinos'].prefix, ])
        if '+libmesh' in spec:
            tpl_list = tpl_list + ";LIBMESH"
            options.extend(['-DTPL_LIBMESH_INSTALL_DIR=%s' %
                            spec['libmesh'].prefix, ])
        if '+sundials' in spec:
            tpl_list = tpl_list + ";SUNDIALS"
            options.extend(['-DTPL_SUNDIALS_INSTALL_DIR=%s' %
                            spec['sundials'].prefix, ])
        if '+amp-timer' in spec:
            tpl_list = tpl_list + ";TIMER"
            options.extend(['-DTPL_TIMER_INSTALL_DIR=%s' %
                            spec['amp-timer'].prefix, ])
        options.extend(['-DTPL_LIST=%s' % tpl_list, ])

        return options
