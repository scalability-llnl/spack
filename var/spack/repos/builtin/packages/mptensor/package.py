# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mptensor(CMakePackage):
    """mptensor is parallel C++ libarary for tensor calculations.
       It provides similar interfaces as Numpy and Scipy in Python."""

    homepage = "https://github.com/smorita/mptensor"
    url      = "https://github.com/smorita/mptensor/archive/v0.3.0.tar.gz"

    version('0.3.0', sha256='819395a91551bddb77958615042fcb935a4b67ee37f912b9a2ca5b49c71befae')

    variant('mpi', default=False, description='Build with MPI library')
    variant("doc", default=False, description="build documentation with Doxygen")

    depends_on('cmake@3.6:', type='build')
    depends_on('mpi', when="+mpi")
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when="+mpi")
    depends_on('doxygen@:1.8.11', type="build", when="+doc")

    test_requires_compiler = True

    def cmake_args(self):
        spec = self.spec
        options = []

        if "+mpi" in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs,
            ])
        else:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spack_cc,
                '-DCMAKE_CXX_COMPILER=%s'     % spack_cxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spack_fc,
            ])

        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        options.extend([
            '-DLAPACK_LIBRARIES=%s' % ';'.join(lapack),
            '-DBLAS_LIBRARIES=%s'   % ';'.join(blas),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('BUILD_DOC', 'doc')
        ])

        return options

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources('.')

    def test(self):
        if "+mpi" not in self.spec:
            print("Test of mptensor only runs with +mpi option.")
        else:
            with working_dir(join_path(self.install_test_root, "tests"), create=False):
                make("clean")
                makefile = FileFilter("Makefile")
                makefile.filter("g++", "{0}".format(spack_cxx), string=True)

            with working_dir(join_path(self.install_test_root), create=False):
                makefile = FileFilter("Makefile.option")
                makefile.filter("CXX =.*", "CXX ={0}".format(self.spec["mpi"].mpicxx))
                makefile.filter(
                    "CXXFLAGS =.*", "CXXFLAGS ={0}".format(self.compiler.cxx11_flag)
                )

            math_libs = (
                self.spec["scalapack"].libs
                + self.spec["lapack"].libs
                + self.spec["blas"].libs
            )

            with working_dir(join_path(self.install_test_root, "tests"), create=False):
                make("LDFLAGS={0}".format(math_libs.ld_flags))

                mpirun = self.spec["mpi"].prefix.bin.mpirun
                mpiexec = Executable(mpirun)
                mpiexec("-n", "1", "tensor_test.out")

                # Test of mptensor has checker
                # and checker is abort when check detect any errors.
                print("Test of mptensor PASSED !")
