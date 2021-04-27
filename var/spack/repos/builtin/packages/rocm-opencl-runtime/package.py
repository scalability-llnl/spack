# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmOpenclRuntime(CMakePackage):
    """ROCm OpenCL 2.0 compatible language runtime.
       It Supports offline and in-process/in-memory compilation"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime"
    url      = "https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0',  sha256='0729e6c2adf1e3cf649dc6e679f9cb936f4f423f4954ad9852857c0a53ef799c')
    version('4.0.0',  sha256='d43ea5898c6b9e730b5efabe8367cc136a9260afeac5d0fe85b481d625dd7df1')
    version('3.10.0', sha256='3aa9dc5a5f570320b04b35ee129ce9ff21062d2770df934c6c307913f975e93d')
    version('3.9.0',  sha256='286ff64304905384ce524cd8794c28aee216befd6c9267d4187a12e5a21e2daf')
    version('3.8.0',  sha256='7f75dd1abf3d771d554b0e7b0a7d915ab5f11a74962c92b013ee044a23c1270a')
    version('3.7.0',  sha256='283e1dfe4c3d2e8af4d677ed3c20e975393cdb0856e3ccd77b9c7ed2a151650b')

    depends_on('cmake@3:', type='build')
    depends_on('mesa18~llvm@18.3: swr=none', type='link')
    depends_on('libelf', type='link', when="@3.7.0:3.8.0")
    depends_on('numactl', type='link', when="@3.7.0:")

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hip-rocclr@' + ver, type='build', when='@' + ver)

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and '@3.7.0:' in self.spec:
            incl = self.spec['hip-rocclr'].prefix.include
            flags.append('-I {0}/compiler/lib/include'.format(incl))
            flags.append('-I {0}/elf'.format(incl))

        return (flags, None, None)

    def cmake_args(self):
        args = [
            '-DUSE_COMGR_LIBRARY=yes'
        ]

        return args
