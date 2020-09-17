# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Migraphx(CMakePackage):
    """ AMD's graph optimization engine."""

    homepage = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX"
    url      = "https://github.com/ROCmSoftwarePlatform/AMDMIGraphX/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='5766f3b262468c500be5051a056811a8edfa741734a5c08c4ecb0337b7906377')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('protobuf', type='link')
    depends_on('blaze', type='build')
    depends_on('nlohmann-json', type='link')
    depends_on('py-pybind11', type='build')
    depends_on('msgpack-c', type='link')
    depends_on('half@1.12.0', type='link')
    for ver in ['3.5.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('miopen-hip@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix)
        ]
        return args
