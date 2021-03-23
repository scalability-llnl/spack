# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Nsimd(CMakePackage):
    """NSIMD is a vectorization library that abstracts SIMD programming.
    It was designed to exploit the maximum power of processors
    at a low development cost."""

    homepage = "https://agenium-scale.github.io/nsimd/"
    url      = "https://github.com/agenium-scale/nsimd/archive/v1.0.tar.gz"

    maintainers = ['eschnett']

    version('2.2', sha256='7916bec6c8ea9ddc690a5bfc80fb1b9402f9e1b2a4b4bb6b6bb8eb5a07eb018e')
    version('2.1', sha256='3274f1061d1fac170130b8c75378a6b94580629b3dc1d53db244b51500ee4695')
    # Version 2.0 is disabled since it does not support cmake
    # version('2.0', sha256='b239e98316f93257161b25c8232634884edcee358982a74742981cc9b68da642')
    version('1.0', sha256='523dae83f1d93eab30114321f1c9a67e2006a52595da4c51f121ca139abe0857')

    variant('simd',
            default='none',
            description='SIMD instruction set',
            values=(
                'none',
                'CPU',
                'SSE2', 'SSE42', 'AVX', 'AVX2', 'AVX512_KNL', 'AVX512_SKYLAKE',
                'NEON128', 'AARCH64',
                'SVE', 'SVE128', 'SVE256', 'SVE512', 'SVE1024', 'SVE2048',
                'CUDA', 'ROCM',
            ),
            multi=False)
    variant('optionals', values=any_combination_of('FMA', 'FP16'),
            description='Optional SIMD features',)

    conflicts('simd=none', msg="SIMD instruction set not defined")
    conflicts('simd=SVE128', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=SVE256', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=SVE512', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=SVE1024', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=SVE2048', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=CUDA', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('simd=ROCM', when=('@:1'),
              msg="SIMD extension not available in version @:1")
    conflicts('optionals=FMA', when=('@2:'),
              msg="SIMD optionals not available in version @2:")
    conflicts('optionals=FP16', when=('@2:'),
              msg="SIMD optionals not available in version @2:")
    conflicts('optionals=FMA,FP16', when=('@2:'),
              msg="SIMD optionals not available in version @2:")

    # Requires a C++14 compiler for building.
    # The C++ interface requires a C++11 compiler to use.
    depends_on('cmake@2.8.7:', type='build')
    depends_on('cmake@3.0.2:', type='build', when='@2:')
    depends_on('python@3:', type='build')

    # Add a 'generate_code' phase in the beginning
    phases = ['generate_code'] + CMakePackage.phases

    def generate_code(self, spec, prefix):
        """Auto-generates code in the build directory"""
        if self.spec.satisfies("@:1"):
            options = [
                'egg/hatch.py',
                '--all',
                '--force',
            ]
            python = spec['python'].command
            python(*options)

    def cmake_args(self):
        # Required SIMD argument
        simd = self.spec.variants['simd'].value
        if self.spec.satisfies("@:1"):
            cmake_args = ["-DSIMD={0}".format(simd)]
        else:
            cmake_args = ["-Dsimd={0}".format(simd)]

        if self.spec.satisfies("@:1"):
            # Optional SIMD instructions to be turned on explicitly
            optionals_value = self.spec.variants['optionals'].value
            if optionals_value != 'none':
                optionals_arg = ';'.join(optionals_value)
                cmake_args.append("-DSIMD_OPTIONALS={0}".format(optionals_arg))

        return cmake_args
