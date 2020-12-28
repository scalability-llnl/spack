# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAutograd(PythonPackage):
    """Autograd can automatically differentiate native Python and
    Numpy code. It can handle a large subset of Python's features,
    including loops, ifs, recursion and closures, and it can even take
    derivatives of derivatives of derivatives. It supports
    reverse-mode differentiation (a.k.a. backpropagation), which means
    it can efficiently take gradients of scalar-valued functions with
    respect to array-valued arguments, as well as forward-mode
    differentiation, and the two can be composed arbitrarily. The main
    intended application of Autograd is gradient-based
    optimization. For more information, check out the tutorial and the
    examples directory."""

    homepage = "https://github.com/HIPS/autograd"
    url      = "https://pypi.io/packages/source/a/autograd/autograd-1.3.tar.gz"

    version('1.3', sha256='a15d147577e10de037de3740ca93bfa3b5a7cdfbc34cfb9105429c3580a33ec4')

    depends_on('py-setuptools', type='build')
    depends_on('py-future@0.15.2:', type=('build', 'run'))
    depends_on('py-numpy@1.12:', type=('build', 'run'))
