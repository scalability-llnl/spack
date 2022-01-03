# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spectre(CMakePackage):
    """The SpECTRE numerical relativity code.

    SpECTRE is an open-source code for multi-scale, multi-physics problems in
    astrophysics and gravitational physics. In the future, we hope that it can
    be applied to problems across discipline boundaries in fluid dynamics,
    geoscience, plasma physics, nuclear physics, and engineering. It runs at
    petascale and is designed for future exascale computers.

    SpECTRE is being developed in support of our collaborative Simulating
    eXtreme Spacetimes (SXS) research program into the multi-messenger
    astrophysics of neutron star mergers, core-collapse supernovae, and
    gamma-ray bursts."""

    homepage = "https://spectre-code.com"
    url = "https://github.com/sxs-collaboration/spectre/archive/v2021.12.15.tar.gz"
    git = "https://github.com/sxs-collaboration/spectre.git"

    maintainers = ['nilsleiffischer']

    generator = 'Ninja'

    version('develop', branch='develop')
    version('2022.01.03', sha256='872a0d152c19864ad543ddcc585ce30baaad4185c2617c13463d780175cbde5f')
    version('2021.12.15', sha256='4bfe9e27412e263ffdc6fcfcb84011f16d34a9fdd633ad7fc84a34c898f67e5c')

    # Configuration variants
    variant('executables',
            values=any_combination_of(
                # CCE
                'CharacteristicExtract', 'ReduceCceWorldtube',
                # Elliptic / initial data
                'SolvePoisson1D', 'SolvePoisson2D', 'SolvePoisson3D',
                'SolveElasticity2D', 'SolveElasticity3D', 'SolveXcts',
                # Tools
                'ExportCoordinates1D', 'ExportCoordinates2D',
                'ExportCoordinates3D',
            ),
            description="Executables to install")
    variant('python', default=False, description="Build Python bindings")
    variant('doc', default=False, description="Build documentation")
    # TODO: support installation of executables with shared libs
    # variant('shared',
    #         default=False,
    #         description="Build shared libraries instead of static")
    variant('memory_allocator',
            values=('system', 'jemalloc'),
            multi=False,
            default='system',
            description="Which memory allocator to use")
    variant('formaline',
            default=True,
            description=("Write the source tree into simulation output files "
                         "to increase reproducibility of results"))
    variant('profiling',
            default=False,
            description="Enable options to make profiling SpECTRE easier")

    # Compiler support
    conflicts('%gcc@:6')
    conflicts('%clang@:7')
    conflicts('%apple-clang@:10')

    # Build dependencies
    depends_on('cmake@3.12:', type='build')
    depends_on('ninja', type='build')
    depends_on('python@2.7:', type='build')

    # Link dependencies
    depends_on('charmpp@6.10.2:')
    depends_on('blaze@3.8')
    depends_on('boost@1.60:+math+program_options')
    depends_on('brigand@master')
    depends_on('gsl')
    # Require HDF5 without MPI, because the SpECTRE build system doesn't try to
    # find and include MPI when CMake reports `HDF5_IS_PARALLEL`, so HDF5 will
    # fail to include MPI headers (as of version 2022.01.03).
    depends_on('hdf5~mpi')
    depends_on('jemalloc', when='memory_allocator=jemalloc')
    depends_on('libsharp~mpi~openmp')
    depends_on('libxsmm@1.16.1:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('yaml-cpp@0.6:')

    # Test dependencies
    depends_on('catch2@2.8:', type='test')
    depends_on('py-numpy@1.10:', type='test')
    depends_on('py-scipy', type='test')
    depends_on('py-h5py', type='test')

    # Python bindings
    with when('+python'):
        extends('python')
        depends_on('python@3.7:', type=('build', 'run'))
        depends_on('py-pybind11@2.6:', type='build')
        depends_on('py-numpy@1.10:', type=('build', 'run'))
        depends_on('py-scipy', type=('build', 'run'))
        depends_on('py-matplotlib', type=('build', 'run'))
        depends_on('py-h5py', type=('build', 'run'))

    # Docs
    with when('+doc'):
        depends_on('doxygen', type='build')
        depends_on('py-beautifulsoup4', type='build')
        depends_on('py-pybtex', type='build')

    # These patches backport updates to the SpECTRE build system to earlier
    # releases, to support installing them with Spack. In particular, we try to
    # support releases associated with published papers, so their results are
    # reproducible.
    # - Backport installation of targets, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/fe3514117c8205dbf18c4d42ec17712e67d33251
    patch('install-pre-2022.01.03.patch', when='@:2022.01.03')
    # - Backport experimental support for Charm++ v7+
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/a2203824ef38ec79a247703ae8cd215befffe391.patch',
        sha256='eb6094028530d9f28cb9c91a90b4af908cc537c8525fb4c81b11c74fd0354932',
        when='@:2022.01.03 ^charmpp@7.0.0:')
    # - Backport IWYU toggle to avoid CMake configuration issues
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/cffeba1bc24bf7c00ec8bac710f02d3db36fa111.patch',
        sha256='912877d4f553adff8b6df8264c50600c1e6d5a9c3ad18be0b86c9d801c07699c',
        when='@:2022.01.03')
    # - Backport patch for Boost 1.77
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/001fc190a6ec73ad6c19ada9444d04a2320f2b96.patch',
        sha256='bf539feb01d01e178889828dbbe5e990e8ee58c9e971d8634845c70a7cfb42a9',
        when='@:2022.01.03 ^boost@1.77:')
    # - Backport patch for Python 3.10 in tests
    patch(
        'https://github.com/sxs-collaboration/spectre/commit/82ff2c39cdae0ecc1e42bdf4564506a4ca869818.patch',
        sha256='5a5a3abf102e92812933e7318daabe2ca0a5a00d81d9663731c527e5dc6c8ced',
        when='@:2022.01.03 ^python@3.10:')
    # - Backport `BUILD_TESTING` toggle, based on upstream patch:
    #   https://github.com/sxs-collaboration/spectre/commit/79bed6cad6e95efadf48a5846f389e90801202d4
    patch('build-testing-pre-2022.01.03.patch', when='@:2022.01.03')

    def cmake_args(self):
        args = [
            self.define('CHARM_ROOT', self.spec['charmpp'].prefix),
            # self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('Python_EXECUTABLE', self.spec['python'].command.path),
            self.define_from_variant('BUILD_PYTHON_BINDINGS', 'python'),
            self.define('BUILD_TESTING', self.run_tests),
            self.define('USE_GIT_HOOKS', False),
            self.define('USE_IWYU', False),
            self.define_from_variant('USE_FORMALINE', 'formaline'),
            self.define_from_variant('MEMORY_ALLOCATOR').upper(),
            self.define_from_variant('ENABLE_PROFILING', 'profiling'),
            # TODO: Fix PCH builds to reduce compile time
            self.define('USE_PCH', False),
        ]
        # Allow for more time on slower machines
        if self.run_tests:
            args.append(self.define('SPECTRE_TEST_TIMEOUT_FACTOR', '10'))
        return args

    @property
    def build_targets(self):
        spec = self.spec
        targets = list(self.spec.variants['executables'].value)
        if 'none' in targets:
            targets.remove('none')
        if '+python' in spec:
            targets.append('all-pybindings')
        if '+doc' in spec:
            targets.append('doc')
        if self.run_tests:
            targets.append('unit-tests')
        if len(targets) == 0:
            raise InstallError("Specify at least one target to build. See "
                               "'spack info spectre' for available targets.")
        return targets

    @run_after('install')
    def install_docs(self):
        if '+doc' in self.spec:
            with working_dir(self.build_directory):
                install_tree(join_path('docs', 'html'), self.prefix.docs)

    @property
    def archive_files(self):
        # Archive the `BuildInfo.txt` file for debugging builds
        return super(Spectre, self).archive_files + [
            join_path(self.build_directory, 'BuildInfo.txt')
        ]

    def check(self):
        with working_dir(self.build_directory):
            # The test suite contains a lot of tests. We select only those
            # related to the targets that were specified.
            # - Unit tests
            ctest('--output-on-failure', '-L', 'unit')
            # - Input file tests for the specified executables
            for executable in self.spec.variants['executables'].value:
                if executable == 'none':
                    continue
                ctest('--output-on-failure', '-L', executable)
