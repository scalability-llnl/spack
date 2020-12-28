# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyScs(PythonPackage):
    """SCS: splitting conic solver"""

    homepage = "https://github.com/cvxgrp/scs"
    url      = "https://www.pypi.io/packages/source/s/scs/scs-2.1.1-2.tar.gz"

    version('2.1.1-2', sha256='f816cfe3d4b4cff3ac2b8b96588c5960ddd2a3dc946bda6b09db04e7bc6577f2')

    variant('cuda', default=False, description="Also compile the GPU CUDA version of SCS")
    variant('float32', default=False, description="Use 32 bit (single precision) floats, default is 64 bit")
    variant('extra_verbose', default=False, description="Extra verbose SCS (for debugging)")
    variant('int32', default=False, description="Use 32 bit ints")
    variant('blas64', default=False, description="Use 64 bit ints for the blas/lapack libs")

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-scipy@0.13.2:', type=('build', 'run'))

    def build_args(self, spec, prefix):
        args = []
        if '+cuda' in spec or '+float32' in spec or '+int32' in spec or\
                '+extra_verbose' in spec or '+blas64' in spec:
            args = ['--scs']
        if '+cuda' in spec:
            args.append('--gpu')
        if '+float32' in spec:
            args.append('--float')
        if '+extra_verbose' in spec:
            args.append('--extraverbose')
        if '+int32' in spec:
            args.append('--int')
        if '+blas64' in spec:
            args.append('--blas64')
        return args
