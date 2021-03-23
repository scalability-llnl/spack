# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class OsuMicroBenchmarks(AutotoolsPackage):
    """The Ohio MicroBenchmark suite is a collection of independent MPI
    message passing performance microbenchmarks developed and written at
    The Ohio State University. It includes traditional benchmarks and
    performance measures such as latency, bandwidth and host overhead
    and can be used for both traditional and GPU-enhanced nodes."""

    homepage = "http://mvapich.cse.ohio-state.edu/benchmarks/"
    url      = "http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.6.3.tar.gz"

    version('5.7',   sha256='1470ebe00eb6ca7f160b2c1efda57ca0fb26b5c4c61148a3f17e8e79fbf34590')
    version('5.6.3', sha256='c5eaa8c5b086bde8514fa4cac345d66b397e02283bc06e44cb6402268a60aeb8')
    version('5.6.2', sha256='2ecb90abd85398786823c0716d92448d7094657d3f017c65d270ffe39afc7b95')
    version('5.6.1', sha256='943c426a653a6c56200193d747755efaa4c4e6f23b3571b0e3ef81ecd21b1063')
    version('5.5',   sha256='1e5a4ae5ef2b03143a815b21fefc23373c1b079cc163c2fa1ed1e0c9b83c28ad')
    version('5.4',   sha256='e1ca762e13a07205a59b59ad85e85ce0f826b70f76fd555ce5568efb1f2a8f33')
    version('5.3',   sha256='d7b3ad4bee48ac32f5bef39650a88f8f2c23a3050b17130c63966283edced89b')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('mpi')
    depends_on('cuda', when='+cuda')

    def configure_args(self):
        spec = self.spec
        config_args = [
            'CC=%s'  % spec['mpi'].mpicc,
            'CXX=%s' % spec['mpi'].mpicxx
        ]

        if '+cuda' in spec:
            config_args.extend([
                '--enable-cuda',
                '--with-cuda=%s' % spec['cuda'].prefix,
            ])

        # librt not available on darwin (and not required)
        if not sys.platform == 'darwin':
            config_args.append('LDFLAGS=-lrt')

        return config_args

    def setup_run_environment(self, env):
        mpidir = join_path(self.prefix.libexec, 'osu-micro-benchmarks', 'mpi')
        env.prepend_path('PATH', join_path(mpidir, 'startup'))
        env.prepend_path('PATH', join_path(mpidir, 'pt2pt'))
        env.prepend_path('PATH', join_path(mpidir, 'one-sided'))
        env.prepend_path('PATH', join_path(mpidir, 'collective'))
