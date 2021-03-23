# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.boost import Boost


class Flecsi(CMakePackage):
    '''FleCSI is a compile-time configurable framework designed to support
       multi-physics application development. As such, FleCSI attempts to
       provide a very general set of infrastructure design patterns that can
       be specialized and extended to suit the needs of a broad variety of
       solver and data requirements. Current support includes multi-dimensional
       mesh topology, mesh geometry, and mesh adjacency information,
       n-dimensional hashed-tree data structures, graph partitioning
       interfaces,and dependency closures.
    '''
    homepage = 'http://flecsi.org/'
    git      = 'https://github.com/laristra/flecsi.git'

    version('devel', branch='devel', submodules=False, preferred=False)
    version('1', branch='1', submodules=False, preferred=False)
    version('1.4', branch='1.4', submodules=False, preferred=True)

    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build', multi=False)
    variant('backend', default='mpi', values=('serial', 'mpi', 'legion', 'hpx', 'charmpp'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('minimal', default=False,
            description='Disable FindPackageMetis')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('flog', default=False,
            description='Enable flog testing')
    variant('doxygen', default=False,
            description='Enable doxygen')
    variant('doc', default=False,
            description='Enable documentation')
    variant('coverage', default=False,
            description='Enable coverage build')
    variant('hdf5', default=True,
            description='Enable HDF5 Support')
    variant('caliper', default=False,
            description='Enable Caliper Support')
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
            description='Build FleCSI Static Analyzer')
    variant('cinch', default=False,
            description='Enable External Cinch')

    depends_on('cmake@3.12:')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build', when='+cinch')
    depends_on('mpi', when='backend=mpi')
    depends_on('mpi', when='backend=legion')
    depends_on('mpi', when='backend=hpx')
    depends_on('legion+shared+mpi', when='backend=legion')
    depends_on('legion+hdf5', when='backend=legion +hdf5')
    depends_on('legion build_type=Debug', when='backend=legion +debug_backend')
    depends_on('hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128', when='backend=hpx')
    depends_on('hpx build_type=Debug', when='backend=hpx +debug_backend')
    depends_on('boost@1.70.0: cxxstd=17 +program_options')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('googletest@1.8.1+gmock')
    depends_on('hdf5+hl+mpi', when='+hdf5')
    depends_on('caliper@2.0.1~adiak', when='+caliper')
    depends_on('graphviz', when='+graphviz')
    depends_on('python@3.0:', when='+tutorial')
    depends_on('doxygen', when='+doxygen')
    depends_on('llvm', when='+flecstan')
    depends_on('pfunit@3.0:3.99')

    conflicts('+tutorial', when='backend=hpx')
    # conflicts('+hdf5', when='backend=hpx')

    def cmake_args(self):
        spec = self.spec
        options = ['-DENABLE_OPENMP=ON',
                   '-DCXX_CONFORMANCE_STANDARD=c++17',
                   '-DENABLE_METIS=ON',
                   '-DENABLE_PARMETIS=ON',
                   '-DENABLE_COLORING=ON',
                   '-DENABLE_DEVEL_TARGETS=ON'
                   ]

        if '+cinch' in spec:
            options.append('-DCINCH_SOURCE_DIR=' + spec['cinch'].prefix)

        if spec.variants['backend'].value == 'legion':
            options.append('-DFLECSI_RUNTIME_MODEL=legion')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'mpi':
            options.append('-DFLECSI_RUNTIME_MODEL=mpi')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'hpx':
            options.append('-DFLECSI_RUNTIME_MODEL=hpx')
            options.append('-DENABLE_MPI=ON')
            options.append('-DHPX_IGNORE_CMAKE_BUILD_TYPE_COMPATIBILITY=ON')
        elif spec.variants['backend'].value == 'charmpp':
            options.append('-DFLECSI_RUNTIME_MODEL=charmpp')
            options.append('-DENABLE_MPI=ON')
        else:
            options.append('-DFLECSI_RUNTIME_MODEL=serial')
            options.append('-DENABLE_MPI=OFF')

        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')

        if '+minimal' in spec:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=ON')
        else:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=OFF')
        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+hdf5' in spec and spec.variants['backend'].value != 'hpx':
            options.append('-DENABLE_HDF5=ON')
        else:
            options.append('-DENABLE_HDF5=OFF')
        if '+caliper' in spec:
            options.append('-DENABLE_CALIPER=ON')
        else:
            options.append('-DENABLE_CALIPER=OFF')
        if '+tutorial' in spec:
            options.append('-DENABLE_FLECSIT=ON')
            options.append('-DENABLE_FLECSI_TUTORIAL=ON')
        else:
            options.append('-DENABLE_FLECSIT=OFF')
            options.append('-DENABLE_FLECSI_TUTORIAL=OFF')

        if '+flecstan' in spec:
            options.append('-DENABLE_FLECSTAN=ON')
        else:
            options.append('-DENABLE_FLECSTAN=OFF')

        if '+doxygen' in spec:
            options.append('-DENABLE_DOXYGEN=ON')
        else:
            options.append('-DENABLE_DOXYGEN=OFF')
        if '+doc' in spec:
            options.append('-DENABLE_DOCUMENTATION=ON')
        else:
            options.append('-DENABLE_DOCUMENTATION=OFF')
        if '+coverage' in spec:
            options.append('-DENABLE_COVERAGE_BUILD=ON')
        else:
            options.append('-DENABLE_COVERAGE_BUILD=OFF')

        return options
