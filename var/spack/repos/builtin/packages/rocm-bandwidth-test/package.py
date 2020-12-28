# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmBandwidthTest(CMakePackage):
    """Test to measure PciE bandwidth on ROCm platforms"""

    homepage = "https://github.com/RadeonOpenCompute/rocm_bandwidth_test"
    url      = "https://github.com/RadeonOpenCompute/rocm_bandwidth_test/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='ad1dedad9023ccb050082c866fa5131665d9c3b50de0b78e4618730c29a07773')
    version('3.9.0', sha256='f366299b48a29b419febb2ba398d1abe4cd01425d33254777e426966b722d3b1')
    version('3.8.0', sha256='7de71a2ba17bbeea9107f2e9e65729f507234d6cbbb44f251240d64683027497')
    version('3.7.0', sha256='9aa1d4b7b01ee4d443effc76ed5f6f43a051fd815692b59dfccf0ecbfeaeed03')
    version('3.5.0', sha256='fbb63fb8713617fd167d9c1501acbd92a6b189ee8e1a8aed668fa6666baae389')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0']:
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)

    build_targets = ['package']
