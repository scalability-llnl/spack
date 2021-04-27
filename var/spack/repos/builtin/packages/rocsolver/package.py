# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocsolver(CMakePackage):
    """rocSOLVER is a work-in-progress implementation of a
       subset of LAPACK functionality on the ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSOLVER"
    git      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='da5cc800dabf7367b02b73c93780b2967f112bb45232e4b06e5fd07b4d5b8d88')
    version('4.0.0', sha256='be9a52644c276813f76d78f2c11eddaf8c2d7f9dd04f4570f23d328ad30d5880')
    version('3.10.0', sha256='bc72483656b6b23a1e321913a580ca460da3bc5976404647536a01857f178dd2')
    version('3.9.0', sha256='85fd77fe5acf5af518d11e90e2c03ee0c5abd61071cea86ef5df09f944879648')
    version('3.8.0', sha256='72aa74284944d8b454088e8c8d74cf05464a4e2e46d33a57017ddd009113025e')
    version('3.7.0', sha256='8c1c630595952806e658c539fd0f3056bd45bafc22b57f0dd10141abefbe4595')
    version('3.5.0', sha256='d655e8c762fb9e123b9fd7200b4258512ceef69973de4d0588c815bc666cb358')

    depends_on('cmake@3:', type='build')
    depends_on('numactl', type='link', when='@3.7.0:')

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        incl = self.spec['rocblas'].prefix
        args = [
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF',
            '-DBUILD_CLIENTS_BENCHMARKS=OFF'
        ]
        if self.spec.satisfies('@4.1.0:'):
            args.append('-DCMAKE_CXX_FLAGS:String=-I{0}/rocblas/include'.format(incl))

        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
