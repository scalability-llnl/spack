# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Formetis(CMakePackage):
    """Automated Fortran bindings to METIS and ParMETIS."""

    homepage = "https://github.com/swig-fortran/formetis"
    url      = "https://github.com/swig-fortran/formetis/archive/refs/tags/v0.0.1.tar.gz"

    maintainers = ['sethrj']

    version('0.0.2', sha256='d0d778fd76185d395041f8bc0ecc2b1f3785cf55db31eb77323bd7cce741c5cb')

    variant('mpi', default=False, description='Enable ParMETIS support')
    variant('shared', default=True, description='Build shared libraries')
    variant('swig', default=False,
            description='Regenerate source files using SWIG')

    depends_on('metis@5')
    depends_on('parmetis', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('swig@4.0.2-fortran', when='+swig')

    # Using non-standard int sizes requires regenerating the C/Fortran
    # interface files with SWIG
    conflicts('~swig', when='^metis+int64')
    conflicts('~swig', when='^metis+real64')

    def cmake_args(self):
        from_variant = self.define_from_variant
        args = [
            from_variant('FORMETIS_USE_MPI', 'mpi'),
            from_variant('BUILD_SHARED_LIBS', 'shared'),
            from_variant('FORMETIS_USE_SWIG', 'swig'),
            self.define('FORMETIS_BUILD_EXAMPLES', False),
        ]
        return args

    examples_src_dir = 'example'

    @run_after('install')
    def setup_smoke_tests(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir])

    def test(self):
        example_src_dir = join_path(self.install_test_root,
                                    self.examples_src_dir)
        test_build_dir = join_path(self.test_suite.stage,
                                   'build_example')

        cmake_args = [
            self.define('CMAKE_PREFIX_PATH', self.prefix),
            self.define('CMAKE_Fortran_COMPILER', self.compiler.fc),
            self.define('METIS_ROOT', self.spec['metis'].prefix),
        ]
        if '+mpi' in self.spec:
            cmake_args.append(
                self.define('ParMETIS_ROOT', self.spec['parmetis'].prefix))
        cmake_args.append(example_src_dir)
        with working_dir(test_build_dir, create=True):
            cmake(*cmake_args)
            make()
            self.run_test('metis', [], [], installed=False,
                          purpose='test: installation')
