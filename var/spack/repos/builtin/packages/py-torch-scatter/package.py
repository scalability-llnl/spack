# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchScatter(PythonPackage):
    """This package consists of a small extension library of
    highly optimized sparse update (scatter and segment)
    operations for the use in PyTorch, which are missing in the
    main package."""

    homepage = "https://github.com/rusty1s/pytorch_scatter"
    url      = "https://github.com/rusty1s/pytorch_scatter/archive/2.0.5.tar.gz"

    version('2.0.5', sha256='e29b364beaa9c84a99e0e236be89ed19d4452d89010ff736184ddcce488b47f6')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-torch+cuda', when='+cuda')
    depends_on('py-torch~cuda', when='~cuda')

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
