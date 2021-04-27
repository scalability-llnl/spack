# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import shutil


class RocmSmiLib(CMakePackage):
    """It is a C library for Linux that provides a user space interface
       for applications to monitor and control GPU applications."""

    homepage = "https://github.com/RadeonOpenCompute/rocm_smi_lib"
    git      = "https://github.com/RadeonOpenCompute/rocm_smi_lib.git"
    url      = "https://github.com/RadeonOpenCompute/rocm_smi_lib/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')
    version('4.1.0', sha256='0c1d2152e40e14bb385071ae16e7573290fb9f74afa5ab887c54f4dd75849a6b')
    version('4.0.0', sha256='93d19229b5a511021bf836ddc2a9922e744bf8ee52ee0e2829645064301320f4')
    version('3.10.0', sha256='8bb2142640d1c6bf141f19accf809e61377a6e0c0222e47ac4daa5da2c85ddac')
    version('3.9.0', sha256='b2934b112542af56de2dc1d5bffff59957e21050db6e3e5abd4c99e46d4a0ffe')
    version('3.8.0', sha256='86250c9ae9dfb18d4f7259a5f2f09b21574d4996fe5034a739ce63a27acd0082')
    version('3.7.0', sha256='72d2a3deda0b55a2d92833cd648f50c7cb64f8341b254a0badac0152b26f1391')
    version('3.5.0', sha256='a5d2ec3570d018b60524f0e589c4917f03d26578443f94bde27a170c7bb21e6e')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    @run_after('install')
    def post_install(self):
        shutil.rmtree(self.prefix.lib)
        install_tree(self.prefix.rocm_smi,  self.prefix)
        shutil.rmtree(self.prefix.rocm_smi)
