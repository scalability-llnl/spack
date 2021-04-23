# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorpack(PythonPackage):
    """Tensorpack is a neural network training interface based
    on TensorFlow."""

    homepage = "https://github.com/tensorpack/tensorpack"
    pypi = "tensorpack/tensorpack-0.10.1.tar.gz"

    maintainers = ['aweits']

    version('0.10.1', sha256='ae6af59794459de910725d268061f0c86d78f01948f9fd5d7b11dd9770ad71ef')
    version('0.9.8', sha256='bc6566c12471a0f9c0a79acc3d045595b1943af8e423c5b843986b73bfe5425f')

    depends_on('python@3.3:', when='@0.10.1:', type=('build', 'run'))
    depends_on('py-setuptools@31:', type='build')
    depends_on("py-numpy@1.14:", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'))
    depends_on("py-termcolor@1.1:", type=('build', 'run'))
    depends_on("py-tabulate@0.7.7:", type=('build', 'run'))
    depends_on("py-tqdm@4.29.0.1:", type=('build', 'run'))
    depends_on("py-msgpack@0.5.2:", type=('build', 'run'))
    depends_on("py-msgpack-numpy@0.4.4.2:", type=('build', 'run'))
    depends_on("py-pyzmq@16:", type=('build', 'run'))
    depends_on("py-psutil@5:", type=('build', 'run'))
    depends_on('py-subprocess32', when='@:0.9.8 ^python@:2.999', type=('build', 'run'))
    depends_on('py-functools32',  when='@:0.9.8 ^python@:2.999', type=('build', 'run'))
