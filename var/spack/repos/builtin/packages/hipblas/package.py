# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipblas(CMakePackage):
    """hipBLAS is a BLAS marshalling library, with multiple
       supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    git      = "https://github.com/ROCmSoftwarePlatform/hipBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-4.1.0.tar.gz"

    version('4.1.0', sha256='876efe80a4109ad53d290d2921b3fb425b4cb857b32920819f10dcd4deee4ef8')
    version('4.0.0', sha256='6cc03af891b36cce8266d32ba8dfcf7fdfcc18afa7a6cc058fbe28bcf8528d94')
    version('3.10.0', sha256='45cb5e3b37f0845bd9e0d09912df4fa0ce88dd508ec9448241ae6600d3c4b1e8')
    version('3.9.0', sha256='82ddd57fd905a5d4060665349ec017ff757a7c121cb9310574be3c3630b3545f')
    version('3.8.0', sha256='33cb82e8b2658ae2096f39e41492ba8b6852ac37c26a730612b8642d9d29abe3')
    version('3.7.0', sha256='9840a493ab4838c86696ceb33ce07c34b5f59f62db4f88cb3af62b69d84f8729')
    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1')

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocsolver@' + ver, when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)

    def cmake_args(self):
        args = [
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF'
        ]

        # hipblas actually prefers CUDA over AMD GPUs when you have it
        # installed...
        if self.spec.satisfies('@:3.9.0'):
            args.append('-DTRY_CUDA=OFF')

        else:
            args.append('-DUSE_CUDA=OFF')

        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
