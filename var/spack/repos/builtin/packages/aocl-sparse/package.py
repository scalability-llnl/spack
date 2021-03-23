# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class AoclSparse(CMakePackage):
    """AOCL-Sparse is a library that contains basic linear algebra subroutines
    for sparse matrices and vectors optimized for AMD EPYC family of processors.
    It is designed to be used with C and C++. Current functionality of sparse
    library supports SPMV function with CSR and ELLPACK formats."""

    homepage = "https://developer.amd.com/amd-aocl/aocl-sparse/"
    url = "https://github.com/amd/aocl-sparse/archive/3.0.tar.gz"
    git = "https://github.com/amd/aocl-sparse.git"

    maintainers = ['amd-toolchain-support']

    version('3.0',  sha256='1d04ba16e04c065051af916b1ed9afce50296edfa9b1513211a7378e1d6b952e')
    version('2.2',  sha256='33c2ed6622cda61d2613ee63ff12c116a6cd209c62e54307b8fde986cd65f664')

    conflicts("%gcc@:9.1.999", msg="Minimum required GCC version is 9.2.0")

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release'))
    variant('shared', default=True,
            description='Build shared library')
    variant('ilp64', default=False,
            description='Build with ILP64 support')

    depends_on('boost', when='@2.2')

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        build_directory = self.stage.source_path

        if self.spec.variants['build_type'].value == 'Debug':
            build_directory = join_path(build_directory, 'build', 'debug')
        else:
            build_directory = join_path(build_directory, 'build', 'release')

        return build_directory

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec

        args = [
            "../..",
            "-DCMAKE_INSTALL_PREFIX:PATH={0}".format(spec.prefix),
            "-DCMAKE_CXX_COMPILER={0}".format(os.path.basename(spack_cxx))
        ]

        if spec.variants['build_type'].value == 'Debug':
            args.append("-DCMAKE_BUILD_TYPE=Debug")
        else:
            args.append("-DCMAKE_BUILD_TYPE=Release")

        args.extend([
            "-DBUILD_SHARED_LIBS:BOOL=%s" % (
                'ON' if '+shared' in spec else 'OFF'),

            "-DBUILD_CLIENTS_BENCHMARKS:BOOL=%s" % (
                'ON' if self.run_tests else 'OFF')
        ])

        if spec.satisfies('@3.0:'):
            args.extend([
                "-DBUILD_ILP64:BOOL=%s" % (
                    'ON' if '+ilp64' in spec else 'OFF')
            ])

        return args

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        """ Simple test to test the built library by running
        one of the aocl-sparse examples, after compiling the
        library with benchmarks.
        """
        dso_suffix = 'so' if '+shared' in self.spec else 'a'

        if self.spec.variants['build_type'].value == 'Debug':
            lib_path = join_path(self.build_directory,
                                 'library',
                                 'libaoclsparse-d.{0}'.format(dso_suffix))
        else:
            lib_path = join_path(self.build_directory,
                                 'library',
                                 'libaoclsparse.{0}'.format(dso_suffix))

        test_bench_bin = join_path(self.build_directory, 'tests',
                                   'staging', 'aoclsparse-bench')
        test_args = " --function=csrmv --precision=d "
        test_args += "--sizem=1000 --sizen=1000 --sizennz=4000 --verify=1 "
        os.system(test_bench_bin + test_args + lib_path)
