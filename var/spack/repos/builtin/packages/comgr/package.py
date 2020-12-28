# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
       contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    url      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-3.10.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.10.0', sha256='b44ee5805a6236213d758fa4b612bb859d8f774b9b4bdc3a2699bb009dd631bc')
    version('3.9.0', sha256='6600e144d72dadb6d893a3388b42af103b9443755ce556f4e9e205ccd8ec0c83')
    version('3.8.0', sha256='62a35480dfabaa98883d91ed0f7c490daa9bbd424af37e07e5d85a6e8030b146')
    version('3.7.0', sha256='73e56ec3c63dade24ad351e9340e2f8e127694028c1fb7cec5035376bf098432')
    version('3.5.0', sha256='25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    # Disable the hip compile tests.  Spack should not be using
    # /opt/rocm, and this breaks the build when /opt/rocm exists.
    patch('hip-tests.patch')

    depends_on('cmake@3.2.0:',  type='build', when='@:3.8.99')
    depends_on('cmake@3.13.4:', type='build', when='@3.9.0:')

    depends_on('zlib', type='link')
    depends_on('z3', type='link')
    depends_on('ncurses', type='link')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0']:
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    root_cmakelists_dir = join_path('lib', 'comgr')
