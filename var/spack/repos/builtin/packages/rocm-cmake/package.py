# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmCmake(CMakePackage):
    """ROCM cmake modules provides cmake modules for common build tasks
       needed for the ROCM software stack"""

    homepage = "https://github.com/RadeonOpenCompute/rocm-cmake"
    git      = "https://github.com/RadeonOpenCompute/rocm-cmake.git"
    url      = "https://github.com/RadeonOpenCompute/rocm-cmake/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('4.1.0', sha256='a4521d119fa07954e529d5e717ad1b338992c0694690dbce00fee26c01129c8c')
    version('4.0.0', sha256='4577487acaa6e041a1316145867584f31caaf0d4aa2dd8fd7f82f81c269cada6')
    version('3.10.0', sha256='751be4484efdcf0d5fa675480db6e2cddab897de4708c7c7b9fa7adb430b52d7')
    version('3.9.0', sha256='e0a8db85bb55acb549f360eb9b04f55104aa93e4c3db33f9ba11d9adae2a07eb')
    version('3.8.0', sha256='9e4be93c76631224eb49b2fa30b0d14c1b3311a6519c8b393da96ac0649d9f30')
    version('3.7.0', sha256='51abfb06124c2e0677c4d6f7fe83c22fe855cb21386f0053ace09f8ab297058b')
    version('3.5.0', sha256='5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    def cmake_args(self):
        return ['-DROCM_DISABLE_LDCONFIG=ON']
