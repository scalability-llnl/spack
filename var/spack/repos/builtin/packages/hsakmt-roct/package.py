# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class HsakmtRoct(CMakePackage):
    """This is a thunk python recipe to build and install Thunk Interface.
       Thunk Interface is a user-mode API interfaces used to interact
       with the ROCk driver."""

    homepage = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface"
    git      = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface.git"
    url      = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('4.1.0', sha256='8443ed5907a7ba9ad4003a49d90ff7b8886e1b2a5e90f14e4035765a7f64d7ca')
    version('4.0.0', sha256='a6960fffc8388731ee18953faae12d1449c582e3b3594418845a544455895f42')
    version('3.10.0', sha256='a3d629247a763cc36f5d48e9122cee8498574af628e14e3c38686c05f66e3e06')
    version('3.9.0', sha256='e1bb8b010855736d8a97957222f648532d42646ec2964776a9a1455dc81104a3')
    version('3.8.0', sha256='cd5440f31f592737b5d05448704bd01f91f73cfcab8a7829922e81332575cfe8')
    version('3.7.0', sha256='b357fe7f425996c49f41748923ded1a140933de7564a70a828ed6ded6d896458')
    version('3.5.0', sha256='d9f458c16cb62c3c611328fd2f2ba3615da81e45f3b526e45ff43ab4a67ee4aa')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('numactl')

    @property
    def install_targets(self):
        if self.version == Version('3.5.0'):
            return ['install', 'install-dev']
        else:
            return ['install']

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS="on"',
        ]
        return args
