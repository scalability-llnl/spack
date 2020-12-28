# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arbor(CMakePackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = "https://github.com/arbor-sim/arbor/"
    url      = "https://github.com/arbor-sim/arbor/archive/v0.2.tar.gz"

    version('0.4', sha256='7d9fc6b3262954cc5dc1751215fbb9f2cdb7010e829a2be43022f90da2d8d2e3')
    version('0.2', sha256='43c9181c03be5f3c9820b2b50592d7b41344f37e1200980119ad347eb7bcf4eb')

    variant('vectorize', default=False,
            description='Enable vectorization of computational kernels')
    variant('gpu', default=False, description='Enable GPU support')
    variant('mpi', default=False, description='Enable MPI support')
    variant('python', default=False,
            description='Enable Python frontend support')
    variant('unwind', default=False,
            description='Enable libunwind for pretty stack traces')

    depends_on('cuda', when='+gpu')
    depends_on('mpi', when='+mpi')
    depends_on('libunwind', when='+unwind')

    extends('python@3.6:', when='+python')
    depends_on('py-mpi4py', when='+mpi+python', type=('build', 'run'))

    depends_on('cmake@3.9:', type='build')
    # mentioned in documentation but shouldn't be necessary when
    # using the archive
    # depends_on('git@2.0:', type='build')

    # compiler dependencies
    # depends_on(C++14)
    # depends_on('gcc@6.1.0:', type='build')
    # depends_on('llvm@4:', type='build')
    # depends_on('clang-apple@9:', type='build')

    # when building documentation, this could be an optional dependency
    depends_on('py-sphinx', type='build')

    conflicts('@:0.2', when='target=aarch64:')

    def patch(self):
        filter_file(
            r'find_library\(_unwind_library_target unwind-\${libunwind_arch}',
            r'find_library(_unwind_library_target unwind-${_libunwind_arch}',
            'cmake/FindUnwind.cmake'
        )
        filter_file(
            r'target_compile_definitions\(arbor-private-deps ARB_WITH_UNWIND\)',      # noqa: E501
            r'target_compile_definitions(arbor-private-deps INTERFACE WITH_UNWIND)',  # noqa: E501
            'CMakeLists.txt'
        )

    def cmake_args(self):
        args = [
            '-DARB_VECTORIZE=' + ('ON' if '+vectorize' in self.spec else 'OFF'),      # noqa: E501
            '-DARB_WITH_GPU=' + ('ON' if '+gpu' in self.spec else 'OFF'),
            '-DARB_WITH_PYTHON=' + ('ON' if '+python' in self.spec else 'OFF'),
        ]

        if '+unwind' in self.spec:
            args.append('-DUnwind_ROOT_DIR={0}'.format(self.spec['libunwind'].prefix))  # noqa: E501

        return args
