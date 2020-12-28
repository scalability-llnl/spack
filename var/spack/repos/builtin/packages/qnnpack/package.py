# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qnnpack(CMakePackage):
    """QNNPACK (Quantized Neural Networks PACKage) is a mobile-optimized
    library for low-precision high-performance neural network inference.
    QNNPACK provides implementation of common neural network operators on
    quantized 8-bit tensors."""

    homepage = "https://github.com/pytorch/QNNPACK"
    git      = "https://github.com/pytorch/QNNPACK.git"

    version('master', branch='master')

    depends_on('cmake@3.5:', type='build')

    resource(
        name='cpuinfo',
        git='https://github.com/Maratyszcza/cpuinfo.git',
        destination='deps',
        placement='cpuinfo'
    )
    resource(
        name='fp16',
        git='https://github.com/Maratyszcza/FP16.git',
        destination='deps',
        placement='fp16'
    )
    resource(
        name='fxdiv',
        git='https://github.com/Maratyszcza/FXdiv.git',
        destination='deps',
        placement='fxdiv'
    )
    resource(
        name='googlebenchmark',
        url='https://github.com/google/benchmark/archive/v1.4.1.zip',
        sha256='61ae07eb5d4a0b02753419eb17a82b7d322786bb36ab62bd3df331a4d47c00a7',
        destination='deps',
        placement='googlebenchmark',
    )
    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.8.0.zip',
        sha256='f3ed3b58511efd272eb074a3a6d6fb79d7c2e6a0e374323d1e6bcbcc1ef141bf',
        destination='deps',
        placement='googletest',
    )
    resource(
        name='psimd',
        git='https://github.com/Maratyszcza/psimd.git',
        destination='deps',
        placement='psimd'
    )
    resource(
        name='pthreadpool',
        git='https://github.com/Maratyszcza/pthreadpool.git',
        destination='deps',
        placement='pthreadpool'
    )

    def cmake_args(self):
        return [
            '-DCPUINFO_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/cpuinfo')),
            '-DFP16_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/fp16')),
            '-DFXDIV_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/fxdiv')),
            '-DPSIMD_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/psimd')),
            '-DPTHREADPOOL_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/pthreadpool')),
            '-DGOOGLEBENCHMARK_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/googlebenchmark')),
            '-DGOOGLETEST_SOURCE_DIR={0}'.format(
                join_path(self.stage.source_path, 'deps/googletest')),
        ]
