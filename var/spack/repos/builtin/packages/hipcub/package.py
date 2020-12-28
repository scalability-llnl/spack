# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipcub(CMakePackage):
    """ Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipCUB"
    url      = "https://github.com/ROCmSoftwarePlatform/hipCUB/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='759da5c6ef0cc1e4ecf2083659e78b8bbaa015f0bb360177674e0feb3032c5be')
    version('3.9.0', sha256='c46995f9f18733ec18e370c21d7c0d6ac719e8e9d3254c6303a20ba90831e12e')
    version('3.8.0', sha256='11d7d97268aeb953c34a80125c4577e27cb57cb6095606533105cecf2bd2ec9c')
    version('3.7.0', sha256='a2438632ea1606e83a8c0e1a8777aa5fdca66d77d90862642eb0ec2314b4978d')
    version('3.5.0', sha256='1eb2cb5f6e90ed1b7a9ac6dd86f09ec2ea27bceb5a92eeffa9c2123950c53b9d')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('numactl', type='link', when='@3.7.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('rocprim@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_MODULE_PATH={0}/cmake'.format(spec['hip'].prefix)
        ]

        return args
