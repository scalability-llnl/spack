# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rdc(CMakePackage):
    """ROCm Data Center Tool"""

    homepage = "https://github.com/RadeonOpenCompute/rdc"
    url      = "https://github.com/RadeonOpenCompute/rdc/archive/rocm-3.8.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        if version == Version('3.9.0'):
            return "https://github.com/RadeonOpenCompute/rdc/archive/rdc_so_ver-0.3.tar.gz"

        url = "https://github.com/RadeonOpenCompute/rdc/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version('4.1.0', sha256='dc81ee9727c8913c05dcf20a00669ce611339ef6d6db8af34e57f42bcfa804ac')
    version('4.0.0', sha256='e9ebfc46dfa983400909ed8a9da4fa37869ab118a8426c2e4f793e21174ca07f')
    version('3.10.0', sha256='fdc51f9f1f756406d1e2ffaeee0e247d1b04fc4078f08e581bbaa7da79697ac1')
    version('3.9.0', sha256='bc6339e7f41850a4a049d085a880cfafd3fd8e1610fb94c572d79753d01aa298')
    version('3.8.0', sha256='d0d0a0e68a848b7a8fa2d88c1d0352ce68e1e142debf32c31d941904f03c4b2f')

    depends_on('cmake@3.15:', type='build')
    depends_on('grpc@1.28.1+shared', type='build')
    depends_on('protobuf', type=('build', 'link'))
    depends_on('libcap', type=('build', 'link'))

    for ver in ['3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('rocm-smi-lib@' + ver, type=('build', 'link'), when='@' + ver)

    def patch(self):
        filter_file(
            r'\${ROCM_DIR}/rocm_smi', '${ROCM_SMI_DIR}', 'CMakeLists.txt')
        filter_file(
            r'${GRPC_ROOT}/bin/protoc',
            '{0}/bin/protoc'.format(self.spec['protobuf'].prefix),
            'CMakeLists.txt', string=True)

    def cmake_args(self):
        rpath = self.rpath
        rpath.append(self.prefix.opt.rocm.rdc.lib)
        rpath = ';'.join(rpath)
        args = ['-DCMAKE_INSTALL_RPATH=' + rpath,
                '-DGRPC_ROOT=' + self.spec['grpc'].prefix,
                '-DCMAKE_MODULE_PATH={0}/cmake_modules'.format
                (self.stage.source_path),
                '-DROCM_SMI_DIR=' + self.spec['rocm-smi-lib'].prefix,
                '-DCMAKE_BUILD_WITH_INSTALL_RPATH=1']
        return args
