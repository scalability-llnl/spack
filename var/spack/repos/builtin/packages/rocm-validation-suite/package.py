# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmValidationSuite(CMakePackage):
    """The ROCm Validation Suite (RVS) is a system administrators
       and cluster manager's tool for detecting and troubleshooting
       common problems affecting AMD GPU(s) running in a high-performance
       computing environment, enabled using the ROCm software stack on a
       compatible platform."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCmValidationSuite"
    url      = "https://github.com/ROCm-Developer-Tools/ROCmValidationSuite/archive/rocm-4.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='f9618f89384daa0ae897b36638a3737bcfa47e98778e360338267cd1fe2bbc66')
    version('4.0.0', sha256='04743ca8901b94a801759a3c13c8caf3e6ea950ffcda6408173e6f9ef7b86e74')
    version('3.10.0', sha256='9f9a530f7850770663e0b0ec0c786367f2e22500a472ac6652c4fd9fb4df4f64')
    version('3.9.0', sha256='17662028a4485b97e3ccaad5e94d20aaa2c3e9e3f741c7ebbf0f8b4cdebcc555')
    version('3.8.0', sha256='68f1c5102e5cbed205a0ecf5a01efbdccf480f7e484ab1e58cbc6bc03e428122')
    version('3.7.0', sha256='bb42d7fb7ee877b80ce53b0cd1f04b0c8301197b6777d2edddcb44732bf8c9e2')
    version('3.5.0', sha256='273e67ecce7e32939341679362b649f3361a36a22fab5f64cefe94b49e6f1e46')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    patch('001-fixes-for-rocblas-rocm-smi-install-prefix-path.patch')
    patch('002-remove-force-setting-hip-inc-path.patch', when='@4.1.0')

    depends_on('cmake@3.5:', type='build')
    depends_on('zlib', type='link')

    def setup_build_environment(self, build_env):
        spec = self.spec
        build_env.set("HIPCC_PATH", spec['hip'].prefix)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hip-rocclr@' + ver, type='build', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('rocminfo@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('rocm-smi-lib@' + ver, type='build', when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        args = ['-DHIP_INC_DIR={0}'.format(spec['hip'].prefix),
                '-DROCM_SMI_DIR={0}'.format(spec['rocm-smi-lib'].prefix),
                '-DROCBLAS_DIR={0}'.format(spec['rocblas'].prefix)]
        return args
