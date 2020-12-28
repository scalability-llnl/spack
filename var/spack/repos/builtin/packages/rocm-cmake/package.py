# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmCmake(CMakePackage):
    """ROCM cmake modules provides cmake modules for common build tasks
       needed for the ROCM software stack"""

    homepage = "https://github.com/RadeonOpenCompute/rocm-cmake"
    url      = "https://github.com/RadeonOpenCompute/rocm-cmake/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='751be4484efdcf0d5fa675480db6e2cddab897de4708c7c7b9fa7adb430b52d7')
    version('3.9.0', sha256='e0a8db85bb55acb549f360eb9b04f55104aa93e4c3db33f9ba11d9adae2a07eb')
    version('3.8.0', sha256='9e4be93c76631224eb49b2fa30b0d14c1b3311a6519c8b393da96ac0649d9f30')
    version('3.7.0', sha256='51abfb06124c2e0677c4d6f7fe83c22fe855cb21386f0053ace09f8ab297058b')
    version('3.5.0', sha256='5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    def cmake_args(self):
        return ['-DROCM_DISABLE_LDCONFIG=ON']
