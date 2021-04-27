# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocprim(CMakePackage):
    """ Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocPRIM"
    git      = "https://github.com/ROCmSoftwarePlatform/rocPRIM.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocPRIM/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('4.1.0', sha256='c46d789f85d15f8ec97f90d67b9d49fb87239912fe8d5f60a7b4c59f9d0e3da8')
    version('4.0.0', sha256='61abf4d51853ae71e54258f43936bbbb096bf06f5891d224d359bfe3104015d0')
    version('3.10.0', sha256='b406956b27d1c06b749e991a250d4ad3eb26e20c6bebf121e2ca6051597b4fa4')
    version('3.9.0', sha256='ace6b4ee4b641280807028375cb0e6fa7b296edba9e9fc09177a5d8d075a716e')
    version('3.8.0', sha256='4d37320d174eaada99dd796d81fa97d5dcc65a6dff8e8ff1c21e8e68acb4ea74')
    version('3.7.0', sha256='225209a0cbd003c241821c8a9192cec5c07c7f1a6ab7da296305fc69f5f6d365')
    version('3.5.0', sha256='29302dbeb27ae88632aa1be43a721f03e7e597c329602f9ca9c9c530c1def40d')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('numactl', type='link', when='@3.7.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
    for ver in ['4.1.0']:
        depends_on('hip-rocclr@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DCMAKE_MODULE_PATH={0}/cmake'.format(spec['hip'].prefix),
            '-DONLY_INSTALL=ON',
            '-DBUILD_TEST=OFF',
            '-DBUILD_BENCHMARK=OFF',
            '-DBUILD_EXAMPLE=OFF'
        ]

        return args
