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

    version('2.2', sha256='e1feb60ac919cf6d233c43c424f6a8a11eab2c62c2c6e3f2652c15ee9063c0c9')
    version('2.1', sha256='3b1d611d46f0f13b3c0917e27012e0f789b23dbefdddcf877b20327552d72fb3')
    version('2.0', sha256='7469680ce955f39d8d6bb7f70d2cc854222e5ef92a39488e77421300a65fad83')
    version('1.3', sha256='6ce42054d63564f57a7276e7c63f3d01ed96a64908b484a99e68309acc968745')
