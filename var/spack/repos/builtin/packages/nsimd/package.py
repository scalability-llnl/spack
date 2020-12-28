# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Nsimd(CMakePackage):
    """NSIMD is a vectorization library that abstracts SIMD programming.
    It was designed to exploit the maximum power of processors
    at a low development cost."""

    homepage = "https://agenium-scale.github.io/nsimd/"
    url      = "https://github.com/agenium-scale/nsimd/archive/v1.0.tar.gz"

    maintainers = ['eschnett']

    version('1.0', sha256='523dae83f1d93eab30114321f1c9a67e2006a52595da4c51f121ca139abe0857')

    variant('simd',
            default='none',
            description='SIMD instruction set',
            values=(
                'none',
                'CPU',
                'SSE2', 'SSE42', 'AVX', 'AVX2', 'AVX512_KNL', 'AVX512_SKYLAKE',
                'NEON128', 'AARCH64', 'SVE',
            ),
            multi=False)
    variant('optionals', values=any_combination_of('FMA', 'FP16'),
            description='Optional SIMD features',)

    conflicts('simd=none', msg="SIMD instruction set not defined")

    # Requires a C++14 compiler for building.
    # The C++ interface requires a C++11 compiler to use.
    depends_on('cmake@2.8.7:', type='build')
    depends_on('python@3:', type='build')

    # Add a 'generate_code' phase in the beginning
    phases = ['generate_code'] + CMakePackage.phases

    def generate_code(self, spec, prefix):
        """Auto-generates code in the build directory"""
        options = [
            'egg/hatch.py',
            '--all',
            '--force',
            '--disable-clang-format',
        ]
        python = spec['python'].command
        python(*options)

    def cmake_args(self):
        # Required SIMD argument
        simd = self.spec.variants['simd'].value
        cmake_args = ["-DSIMD={0}".format(simd)]

        # Optional SIMD instructions to be turned on explicitly
        optionals_value = self.spec.variants['optionals'].value
        if optionals_value != 'none':
            optionals_arg = ';'.join(optionals_value)
            cmake_args.append("-DSIMD_OPTIONALS={0}".format(optionals_arg))

        return cmake_args
