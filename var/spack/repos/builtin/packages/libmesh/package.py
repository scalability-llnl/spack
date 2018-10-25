# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmesh(AutotoolsPackage):
    """The libMesh library provides a framework for the numerical simulation of
       partial differential equations using arbitrary unstructured
       discretizations on serial and parallel platforms."""

    homepage = "http://libmesh.github.io/"
    url      = "https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2"
    git      = "https://github.com/libMesh/libmesh.git"

    version('1.3.0', sha256='a8cc2cd44f42b960989dba10fa438b04af5798c46db0b4ec3ed29591b8359786')
    version('1.2.1', sha256='11c22c7d96874a17de6b8c74caa45d6745d40bf3610e88b2bd28fd3381f5ba70')
    version('1.0.0', 'cb464fc63ea0b71b1e69fa3f5d4f93a4')

    # support for libraries that are only available through the bundled copies:
    # TODO libMesh 1.2.1 gained the ability to specify a path to capnproto
    variant('capnproto', default=False, description='Compile with the bundled capnproto serialization library')
    variant('exodusii', default=False, description='Compile with the bundled ExodusII output library')
    variant('fparser', default=False, description='Compile with the bundled fparser function parser library')
    variant('gmv', default=False, description='Compile with the bundled gmv format IO library')
    variant('laspack', default=False, description='Compile with the bundled laspack interative solver library')
    variant('libhilbert', default=False, description='Compile with the bundled libHilbert partitioning library')
    variant('metaphysicl', default=False, description='Compile with the bundled metaphysicl AD library')
    variant('metis', default=False, description='Compile with the bundled METIS graph partitioning library')
    variant('nanoflann', default=False, description='Compile with the bundled nanoflann graph library')
    variant('nemesis', default=False, description='Compile with the bundled nemesis IO library')
    variant('netcdf', default=False, description='Compile with the bundled NETCDF IO library')
    # TODO parmetis assumes that we use the bundled copy of metis, but the
    # existing build script assumes that we can get METIS from PETSc. Be
    # conservative and completely disable parmetis support for now.
    # variant('parmetis', default=False,
    #         description='Compile with the bundled PARMETIS graph library')
    variant('qhull', default=False, description='Compile with the bundled qhull mesh generation library')
    variant('sfc', default=False, description='Compile with the bundled sfcurves partitioning library')
    variant('tetgen', default=False, description='Compile with the bundled tetgen mesh generation library')
    variant('triangle', default=False, description='Compile with the bundled Triangle mesh generation library')

    # support for libraries that may be externally installed:
    variant('boost', default=False, description='Compile with components dependent on boost')
    variant('eigen', default=False, description='support for dense linear algebra with Eigen')
    variant('hdf5', default=False, description='Compile with support for HDF5 files')
    variant('slepc', default=False, description='Compile with support for the SLEPc eigensolver')

    # other features:
    variant('debug', default=False, description='Compile with support for debugging')
    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('openmp', default=False,
            description='Enable OpenMP support; '
            'this is independent of the choice of threading library')
    variant('threads', default='none', description='Enable threading support',
            values=('none', 'pthreads', 'tbb'), multi=False)

    conflicts('+metaphysicl', when='@:1.2.999',
              msg='The interface to metaphysicl is not available in libMesh '
              'versions older than 1.3.0. Please explicitly disable this '
              'variant.')

    depends_on('boost', when='+boost')
    # The Scotch dependency of Eigen is not used by libMesh. Since Scotch can
    # only be used with certain versions of flex it conflicts with several
    # versions of GCC, so explicitly disable it.
    depends_on('eigen~scotch', when='+eigen')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+slepc')
    # compilation dependencies depend on perl
    depends_on('perl')
    depends_on('petsc+mpi', when='+mpi')
    depends_on('petsc+metis', when='+metis')
    depends_on('slepc', when='+slepc')
    depends_on('tbb', when='threads=tbb')

    def configure_args(self):
        options = []

        # GLIBCXX debugging is not, by default, supported by other libraries,
        # so unconditionally disable it for libmesh
        options.append('--enable-glibcxx-debugging=no')

        # All bundled dependencies are explicitly disabled, so we do not need
        # to perform this check:
        options.append('--disable-strict-lgpl')

        # The Hinnant unique pointer implementation is incompatible with boost
        # (and not necessary with C++11 support), so unconditionally disable
        # it:
        options.append('--disable-hinnant-unique-ptr')
        # libMesh does not allow for us to specify an installation location for
        # zlib, an undocumented dependency of gzstreams: hence we must
        # unconditionally disable gzstreams.
        options.append('--enable-gzstreams=no')
        # Similarly, since we cannot specify a location for bzip2 or xz, so
        # disable them to avoid picking up system installations:
        options.append('--disable-bzip2')
        options.append('--disable-xz')
        # TODO enable GDB backtracing. Disable for now to avoid picking up the
        # system gdb installation:
        options.append('--without-gdb-command')

        # TODO add X11 as a dependency to get tecplot working
        options.append('--enable-tecio=no')
        options.append('--enable-tecplot=no')

        # handle the bundled libraries that are not themselves dependencies of
        # other bundled libaries:
        for bundled_library in ['capnproto', 'exodusii', 'fparser', 'gmv',
                                'laspack', 'libHilbert', 'metaphysicl',
                                'nanoflann', 'nemesis', 'parmetis', 'qhull',
                                'sfc', 'tetgen', 'triangle']:
            if '+' + bundled_library.lower() in self.spec:
                options.append('--enable-' + bundled_library + "=yes")
            else:
                options.append('--enable-' + bundled_library + "=no")

        # and the ones which are dependencies of other bundled libraries:
        if '+exodusii' in self.spec or '+netcdf' in self.spec:
            options.append('--enable-netcdf=yes')
        else:
            options.append('--enable-netcdf=no')

        # handle external library dependencies:
        if '+boost' in self.spec:
            options.append('--with-boost=%s' % self.spec['boost'].prefix)
        else:
            options.append('--enable-boost=no')

        if '+eigen' in self.spec:
            options.append('--with-eigen=%s' % self.spec['eigen'].prefix)
        else:
            options.append('--enable-eigen=no')

        if '+hdf5' in self.spec:
            options.append('--with-hdf5=%s' % self.spec['hdf5'].prefix)
        else:
            options.append('--enable-hdf5=no')
            # This is necessary with libMesh 1.2.1 to prevent a configure
            # error:
            if '+netcdf' not in self.spec:
                options.append('--disable-netcdf-4')

        if '+metis' in self.spec:
            options.append('--with-metis=PETSc')

        if '+petsc' in self.spec:
            options.append('--enable-petsc=yes')
            options.append('PETSC_DIR=%s' % self.spec['petsc'].prefix)
        else:
            options.append('--enable-petsc=no')

        if '+slepc' in self.spec:
            options.append('SLEPC_DIR=%s' % self.spec['slepc'].prefix)
        else:
            options.append('--enable-slepc=no')

        # and, finally, other things:
        if '+debug' in self.spec:
            options.append('--with-methods=dbg')
        else:
            options.append('--with-methods=opt')

        if '+mpi' in self.spec:
            options.append('CC=%s' % self.spec['mpi'].mpicc)
            options.append('CXX=%s' % self.spec['mpi'].mpicxx)
            options.append('--with-mpi=%s' % self.spec['mpi'].prefix)
        else:
            options.append('--disable-mpi')
            # libMesh will try to link with the system MPI library unless we
            # provide explicit overrides
            options.append('CC=%s' % self.compiler.cc)
            options.append('CXX=%s' % self.compiler.cxx)

        if '+openmp' in self.spec:
            options.append('--enable-openmp=yes')
        else:
            options.append('--enable-openmp=no')

        if 'threads=pthreads' in self.spec:
            options.append('--with-thread-model=pthread')
            options.append('--enable-pthreads=yes')
        else:
            options.append('--enable-pthreads=no')

        if 'threads=tbb' in self.spec:
            options.append('--with-thread-model=tbb')
            options.append('--enable-tbb=yes')
            options.append('--with-tbb=%s' % self.spec['tbb'].prefix)
        else:
            options.append('--enable-tbb=no')

        return options

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.append_flags('PERL', self.spec['perl'].command.path)
