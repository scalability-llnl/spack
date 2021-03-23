# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkg.builtin.blis import BlisBase


class Amdblis(BlisBase):
    """AMD Optimized BLIS.

    BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries. The framework was designed to
    isolate essential kernels of computation that, when optimized, immediately
    enable optimized implementations of most of its commonly used and
    computationally intensive operations.
    """

    _name = 'amdblis'
    homepage = "https://developer.amd.com/amd-aocl/blas-library/"
    url = "https://github.com/amd/blis/archive/3.0.tar.gz"
    git = "https://github.com/amd/blis.git"

    maintainers = ['amd-toolchain-support']

    version('3.0', sha256='ac848c040cd6c3550fe49148dbdf109216cad72d3235763ee7ee8134e1528517')
    version('2.2', sha256='e1feb60ac919cf6d233c43c424f6a8a11eab2c62c2c6e3f2652c15ee9063c0c9')

    def configure_args(self):
        spec = self.spec
        args = super(Amdblis, self).configure_args()

        if spec.satisfies('@3.0 %aocc'):
            """ To enabled Fortran to C calling convention for
            complex types when compiling with aocc flang"""
            args.append('CFLAGS={0}'.format("-DAOCL_F2C"))
            args.append('CXXFLAGS={0}'.format("-DAOCL_F2C"))

        return args
