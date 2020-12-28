# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ccls(CMakePackage):
    """C/C++ language server"""

    homepage = "https://github.com/MaskRay/ccls"
    git      = "https://github.com/MaskRay/ccls.git"
    url      = "https://github.com/MaskRay/ccls/archive/0.20201025.tar.gz"

    maintainers = ['jacobmerson']

    version('0.20201025', sha256='1470797b2c1a466e2d8a069efd807aac6fefdef8a556e1edf2d44f370c949221')

    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    depends_on("cmake@3.8:", type="build")
    depends_on('llvm@7:')
    depends_on('rapidjson')
