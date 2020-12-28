# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vc(CMakePackage):
    """SIMD Vector Classes for C++"""

    homepage = "https://github.com/VcDevel/Vc"
    url      = "https://github.com/VcDevel/Vc/archive/1.3.0.tar.gz"

    version('1.4.1', sha256='7e8b57ed5ff9eb0835636203898c21302733973ff8eaede5134dd7cb87f915f6')
    version('1.3.0', sha256='2309a19eea136e1f9d5629305b2686e226093e23fe5b27de3d6e3d6084991c3a')
    version('1.2.0', sha256='9cd7b6363bf40a89e8b1d2b39044b44a4ce3f1fd6672ef3fc45004198ba28a2b')
    version('1.1.0', sha256='281b4c6152fbda11a4b313a0a0ca18565ee049a86f35f672f1383967fef8f501')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebug',
                    'RelWithDebInfo', 'MinSizeRel'))

    def cmake_args(self):
        if self.run_tests:
            return ['-DBUILD_TESTING=ON']
        else:
            return ['-DBUILD_TESTING=OFF']
