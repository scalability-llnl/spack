# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChainer(PythonPackage):
    """
    Chainer is a Python-based deep learning framework aiming at flexibility.

    It provides automatic differentiation APIs based on the define-by-run
    approach (a.k.a. dynamic computational graphs) as well as object-oriented
    high-level APIs to build and train neural networks.
    It also supports CUDA/cuDNN using CuPy for high performance training
    and inference.
    """

    homepage = "https://chainer.org/"
    url      = "https://github.com/chainer/chainer/archive/v7.2.0.tar.gz"

    maintainers = ['adamjstewart']

    version('7.2.0', sha256='6e2fba648cc5b8a5421e494385b76fe5ec154f1028a1c5908557f5d16c04f0b3')
    version('6.7.0', sha256='87cb3378a35e7c5c695028ec91d58dc062356bc91412384ea939d71374610389')

    depends_on('python@3.5.1:', when='@7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
    depends_on('py-typing-extensions@:3.6.6', when='@:6', type=('build', 'run'))
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-protobuf@3:', type=('build', 'run'))
    depends_on('py-typing@:3.6.6', when='@:6', type=('build', 'run'))
