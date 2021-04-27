# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nccl(MakefilePackage, CudaPackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/nccl"
    url      = "https://github.com/NVIDIA/nccl/archive/v2.7.3-1.tar.gz"

    maintainers = ['adamjstewart']

    version('2.9.6-1', sha256='c4b1f5a88f03c0ac8f1dcbe27723cd75cfe051754078d83629efaaed10ce8731')
    version('2.8.4-1', sha256='a5c1b4da6e1608ee63baa87f6df424bba7a8b1cedad597a25d5b4cf8d56d0865')
    version('2.8.3-1', sha256='3ae89ddb2956fff081e406a94ff54ae5e52359f5d645ce977c7eba09b3b782e6')
    version('2.7.8-1', sha256='fa2bec307270f30fcf6280a85f24ea8801e0ce3b3027937c7325260a890b07e0')
    version('2.7.6-1', sha256='60dd9b1743c2db6c05f60959edf98a4477f218115ef910d7ec2662f2fb5cf626')
    version('2.7.5-1', sha256='26a8dec6fa0a776eb71205d618d58e26d372621719788a23b33db6fdce4426bf')
    version('2.7.3-1', sha256='dc7b8794373306e323363314c3327796e416f745e8003490fc1407a22dd7acd6')
    version('2.6.4-1', sha256='ed8c9dfd40e013003923ae006787b1a30d3cb363b47d2e4307eaa2624ebba2ba')
    version('2.5.7-1', sha256='781a6bb2278566be4abbdf22b2fa19afc7306cff4b312c82bd782979b368014e')
    version('2.5.6-2', sha256='8a30e0b4813a825592872fcbeeede22a659e2c399074dcce02960591dc81387d')
    version('2.5.6-1', sha256='38a37d98be11f43232b988719226866b407f08b9666dcaf345796bd8f354ef54')
    version('2.4.8-1', sha256='e2260da448ebbebe437f74768a346d28c74eabdb92e372a3dc6652a626318924')
    version('2.4.6-1', sha256='ea4421061a7b9c454f2e088f68bfdbbcefab80ce81cafc70ee6c7742b1439591')
    version('2.4.2-1', sha256='e3dd04b22eb541394bd818e5f78ac23a09cc549690d5d55d6fccc1a36155385a')
    version('2.3.7-1', sha256='e6eff80d9d2db13c61f8452e1400ca2f098d2dfe42857cb23413ce081c5b9e9b')
    version('2.3.5-5', sha256='bac9950b4d3980c25baa8e3e4541d2dfb4d21edf32ad3b89022d04920357142f')
    version('1.3.4-1', sha256='11e4eb44555bb28b9cbad973dacb4640b82710c9769e719afc2013b63ffaf884')
    version('1.3.0-1', sha256='53f36151061907bdcafad1c26c1d9370a0a8400f561a83704a5138213ba51003')

    variant('cuda', default=True, description='Build with CUDA')

    depends_on('rdma-core', when='@2.3.5-5:')

    # https://github.com/NVIDIA/nccl/issues/244
    patch('so_reuseport.patch', when='@2.3.7-1:2.4.8-1')

    conflicts('~cuda', msg='NCCL requires CUDA')

    @property
    def build_targets(self):
        return ['CUDA_HOME={0}'.format(self.spec['cuda'].prefix)]

    @property
    def install_targets(self):
        if self.version >= Version('2.3.5-5'):
            return ['PREFIX={0}'.format(self.prefix), 'src.install']
        else:
            return ['PREFIX={0}'.format(self.prefix), 'install']
