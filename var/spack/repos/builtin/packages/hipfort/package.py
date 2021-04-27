# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipfort(CMakePackage):
    """ Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipfort"
    git      = "https://github.com/ROCmSoftwarePlatform/hipfort.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipfort/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='2d335ae068d0cbb480575de7d3ea4868362af32cb195f911ee1aeced499f3974')
    version('4.0.0', sha256='a497645c33e0eff39abd5344756de63424733cde2837b7376c924b44ed5ae9c9')
    version('3.10.0', sha256='44173522d9eb2a18ec1cea2d9b00b237fe70501f0849bd6be3decbb73389487a')
    version('3.9.0', sha256='a3c4e125a9b56820446a65bd76b8caa196fddb0e0723eb513f0bcde9abd6a0c0')
    version('3.8.0', sha256='0132e9949f758dd8b8a462d133b3316101440cd503aa6c53bea9e34e61bbb3cc')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
