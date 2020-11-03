# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url = "https://github.com/amd/blis/archive/2.2.tar.gz"
    git = "https://github.com/amd/blis.git"

    maintainers = ['amd-toolchain-support']

    version('2.2', sha256='e1feb60ac919cf6d233c43c424f6a8a11eab2c62c2c6e3f2652c15ee9063c0c9')
