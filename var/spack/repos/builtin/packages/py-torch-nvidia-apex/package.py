# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTorchNvidiaApex(PythonPackage, CudaPackage):
    """A PyTorch Extension: Tools for easy mixed precision and
    distributed training in Pytorch """

    homepage = "https://github.com/nvidia/apex/"
    git      = "https://github.com/nvidia/apex/"

    phases = ['install']

    version('master', branch='master')
    version('2020-10-19', commit='8a1ed9e8d35dfad26fb973996319965e4224dcdd')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-torch@0.4:', type=('build', 'run'))
    depends_on('cuda@9:', when='+cuda')
    depends_on('py-pybind11', type=('build', 'link', 'run'))

    variant('cuda', default=True, description='Build with CUDA')

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            env.set('CUDA_HOME', self.spec['cuda'].prefix)
            if (self.spec.variants['cuda_arch'].value[0] != 'none'):
                torch_cuda_arch = ';'.join(
                    '{0:.1f}'.format(float(i) / 10.0) for i
                    in
                    self.spec.variants['cuda_arch'].value)
                env.set('TORCH_CUDA_ARCH_LIST', torch_cuda_arch)

    def install_args(self, spec, prefix):
        args = super(PyTorchNvidiaApex, self).install_args(spec, prefix)
        if spec.satisfies('^py-torch@1.0:'):
            args.append('--cpp_ext')
            if '+cuda' in spec:
                args.append('--cuda_ext')
        return args
