# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import glob

from spack import *


class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate
       pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocRAND"
    git      = "https://github.com/ROCmSoftwarePlatform/rocRAND.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocRAND/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='94327e38739030ab6719a257f5a928a35842694750c7f46d9e11ff2164c2baed')
    version('4.0.0', sha256='1cafdbfa15cde635bd424d2a858dc5cc94d668f9a211ff39606ee01ed1715f41')
    version('3.10.0', sha256='f55e2b49b4dfd887e46eea049f3359ae03c60bae366ffc979667d364205bc99c')
    version('3.9.0', sha256='a500a3a83be36b6c91aa062dc6eef1f9fc1d9ee62422d541cc279513d98efa91')
    version('3.8.0', sha256='79eb84d41363a46ed9bb18d9757cf6a419d2f48bb6a71b8e4db616a5007a6560')
    version('3.7.0', sha256='5e43fe07afe2c7327a692b3b580875bae6e6ee790e044c053fffafbfcbc14860')
    version('3.5.0', sha256='592865a45e7ef55ad9d7eddc8082df69eacfd2c1f3e9c57810eb336b15cd5732')

    depends_on('cmake@3.5.1:', type='build')
    depends_on('numactl', when='@3.7.0:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocminfo@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
    for ver in ['4.1.0']:
        depends_on('hip-rocclr@' + ver, type='link', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    @run_after('install')
    def fix_library_locations(self):
        """Fix the rocRAND and hipRAND libraries location"""
        # rocRAND installs librocrand.so* and libhiprand.so* to rocrand/lib and
        # hiprand/lib, respectively. This confuses spack's RPATH management. We
        # fix it by adding a symlink to the libraries.
        hiprand_lib_path = join_path(self.prefix, 'hiprand', 'lib')
        rocrand_lib_path = join_path(self.prefix, 'rocrand', 'lib')
        mkdirp(self.prefix.lib)
        with working_dir(hiprand_lib_path):
            hiprand_libs = glob.glob('*.so*')
            for lib in hiprand_libs:
                os.symlink(join_path(hiprand_lib_path, lib),
                           join_path(self.prefix.lib, lib))
        with working_dir(rocrand_lib_path):
            rocrand_libs = glob.glob('*.so*')
            for lib in rocrand_libs:
                os.symlink(join_path(rocrand_lib_path, lib),
                           join_path(self.prefix.lib, lib))

    def cmake_args(self):
        args = ['-DBUILD_BENCHMARK=OFF',
                '-DBUILD_TEST=OFF']
        return args
