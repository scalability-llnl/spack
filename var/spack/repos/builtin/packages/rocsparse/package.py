# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocsparse(CMakePackage):
    """rocSPARSE exposes a common interface that provides
    Basic Linear Algebra Subroutines for sparse computation
    implemented on top of AMD's Radeon Open eCosystem Platform ROCm runtime
    and toolchains. rocSPARSE is created using the HIP programming
    language and optimized for AMD's latest discrete GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    git      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='7514968ed2342dc274acce8b269c128a6aa96cce769a37fd3880b5269c2ed17f')
    version('4.0.0', sha256='2b41bc6623d204ad7f351a902810f34cd32b762d1bf59081dbb00f83e689a794')
    version('3.10.0', sha256='8325828c5d7818dfb45e03b5f1572a573cc21964d596aaaa33b7469817b03abd')
    version('3.9.0', sha256='7b8f952d0c7f8ac2f3bb60879ab420fabbfafb0885a3d8464d5b4c191e97dec6')
    version('3.8.0', sha256='a5d085fffe05a7ac7f5658075d9782b9b02d0c5c3e2c1807dad266c3a61141fd')
    version('3.7.0', sha256='db561ae5e8ee117f7c539a9ef6ee49c13b82ba9f702b22c76e741cca245386a9')
    version('3.5.0', sha256='9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocprim@' + ver, type='build', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='link', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
    for ver in ['4.1.0']:
        depends_on('hip-rocclr@' + ver, type='link', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
