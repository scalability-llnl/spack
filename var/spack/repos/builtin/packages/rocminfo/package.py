# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocminfo(CMakePackage):
    """Radeon Open Compute (ROCm) Runtime rocminfo tool"""

    homepage = "https://github.com/RadeonOpenCompute/rocminfo"
    git      = "https://github.com/RadeonOpenCompute/rocminfo.git"
    url      = "https://github.com/RadeonOpenCompute/rocminfo/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('4.1.0', sha256='5b994ad02b6d250160770f6f7730835f3a52127193ac9a8dee40c53aec911f4f')
    version('4.0.0', sha256='0b3d692959dd4bc2d1665ab3a838592fcd08d2b5e373593b9192ca369e2c4aa7')
    version('3.10.0', sha256='ed02375be3be518b83aea7309ef5ca62dc9b6dbad0aae33e92995102d6d660be')
    version('3.9.0', sha256='9592781e0c62b910c4adc5c7f4c27c7a0cddbed13111a19dd91a2ff43720e43d')
    version('3.8.0', sha256='c135dc98ecb5f420e22a6efd2f461ba9ed90be3f42e2ac29356e05c6a0706f8f')
    version('3.7.0', sha256='86a8e3ce7d91fb2d79688a22a2805757c83922d9f17ea7ea1cb41bf9516197ea')
    version('3.5.0', sha256='1d113f06b7c9b60d0e92b2c12c0c704a565696867496fe7038e5dddd510567b7')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        args = ['-DROCM_DIR={0}'.format(self.spec['hsa-rocr-dev'].prefix)]
        return args
