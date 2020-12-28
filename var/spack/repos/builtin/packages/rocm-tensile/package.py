# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmTensile(CMakePackage):
    """Radeon Open Compute Tensile library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/Tensile/"
    url      = "https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-3.8.0.tar.gz"
    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.8.0', sha256='c78a11db85fdf54bfd26533ee6fa98f6a6e789fa423537993061497ac5f22ed6')
    version('3.7.0', sha256='488a7f76ea42a7601d0557f53068ec4832a2c7c06bb1b511470a4e35599a5a4d')
    version('3.5.0', sha256='71eb3eed6625b08a4cedb539dd9b596e3d4cc82a1a8063d37d94c0765b6f8257')

    amdgpu_targets = ('all', 'gfx803', 'gfx900', 'gfx906', 'gfx908')

    variant('amdgpu_target', default='all', multi=True, values=amdgpu_targets)

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        # used in Tensile
        depends_on('rocm-smi@' + ver, type='build', when='@' + ver)
        depends_on('rocm-smi-lib@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)

    # This is the default library format since 3.7.0
    depends_on('msgpack-c@3:', when='@3.7:')
    depends_on('boost@1.58.0', type=('build', 'link'))

    root_cmakelists_dir = 'Tensile/Source'
    # Status: https://github.com/ROCmSoftwarePlatform/Tensile/commit/a488f7dadba34f84b9658ba92ce9ec5a0615a087
    # Not yet landed in 3.7.0, nor 3.8.0.
    patch('0001-fix-compile-error.patch')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        archs = ",".join(self.spec.variants['amdgpu_target'].value)

        args = [
            '-Damd_comgr_DIR={0}'.format(self.spec['comgr'].prefix),
            '-DTensile_COMPILER=hipcc',
            '-DTensile_ARCHITECTURE={0}'.format(archs),
            '-DTensile_LOGIC=asm_full',
            '-DTensile_CODE_OBJECT_VERSION=V3',
            '-DBoost_USE_STATIC_LIBS=Off',
            '-DBUILD_WITH_TENSILE_HOST={0}'.format(
                'ON' if '@3.7.0:' in self.spec else 'OFF'
            )
        ]

        if '@3.7.0:' in self.spec:
            args.append('-DTensile_LIBRARY_FORMAT=msgpack')

        return args
