# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT/"
    url      = "https://github.com/ROCmSoftwarePlatform/rocfft/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='9f57226aac7d9a0515e14a5a5b08a85e727de72b3f9c2177daf56749ac2c76ae')
    version('3.9.0', sha256='9c9c0b7f09bab17250f5101d1605e7a61218eae828a3eb8fe048d607181294ce')
    version('3.8.0', sha256='ed23009796e2ee7c43dcc24527f2d6b1d7a73dceac06c30384460098d2fe1556')
    version('3.7.0', sha256='94462e4bd19c2c749fcf6903adbee66d4d3bd345c0246861ff8f40b9d08a6ead')
    version('3.5.0', sha256='629f02cfecb7de5ad2517b6a8aac6ed4de60d3a9c620413c4d9db46081ac2c88')

    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012'
    )

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    variant('amdgpu_target', default='gfx701', multi=True, values=amdgpu_targets)

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, type=('build', 'link'), when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        archs = ",".join(self.spec.variants['amdgpu_target'].value)

        args = [
            '-DCMAKE_CXX_FLAGS=--amdgpu-target={0}'.format(archs),
        ]
        return args
