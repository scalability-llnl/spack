# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs"
    url      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='bca9291385d6bdc91a8b39a46f0fd816157d38abb1725ff5222e6a0daa0834cc')
    version('3.9.0', sha256='c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7')
    version('3.8.0', sha256='e82cc9a8eb7d92de02cabb856583e28f17a05c8cf9c97aec5275608ef1a38574')
    version('3.7.0', sha256='b3a114180bf184b3b829c356067bc6a98021d52c1c6f9db6bc57272ebafc5f1d')
    version('3.5.0', sha256='dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('zlib', type='link', when='@3.9.0:')
    depends_on('texinfo', type='link', when='@3.9.0:')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0']:
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def cmake_args(self):
        spec = self.spec
        args = ['-DLLVM_DIR={0}'.format(spec['llvm-amdgpu'].prefix),
                '-DCMAKE_C_COMPILER={0}/bin/clang'.format(
                    spec['llvm-amdgpu'].prefix),
                ]
        return args
