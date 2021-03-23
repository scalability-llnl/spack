# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorchSparse(PythonPackage):
    """This package consists of a small extension library of
    optimized sparse matrix operations with autograd support."""

    homepage = "https://github.com/rusty1s/pytorch_sparse/"
    url      = "https://github.com/rusty1s/pytorch_sparse/archive/0.6.7.tar.gz"

    version('0.6.8', sha256='98f7ff1f0f9cd5031bc81c70c11970c3864545ae33677025a6efd2466a97e6f9')
    version('0.6.7', sha256='0d038a1502548692972a085cd0496460b5d2050bb7328427add990f081d6c44d')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-torch-scatter+cuda', when='+cuda')
    depends_on('py-torch-scatter~cuda', when='~cuda')

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            cuda_arches = list(
                self.spec['py-torch'].variants['cuda_arch'].value)
            for i, x in enumerate(cuda_arches):
                cuda_arches[i] = '{0}.{1}'.format(x[0:-1], x[-1])
            env.set('TORCH_CUDA_ARCH_LIST', str.join(' ', cuda_arches))

            env.set('FORCE_CUDA', '1')
            env.set('CUDA_HOME', self.spec['cuda'].prefix)
        else:
            env.set('FORCE_CUDA', '0')
