# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clara(CMakePackage):
    """A simple to use, composable, command line parser for C++ 11
    and beyond."""

    homepage = "https://github.com/catchorg/Clara"
    url      = "https://github.com/catchorg/Clara/archive/v1.1.5.tar.gz"

    maintainers = ['bvanessen']

    variant('single_header', default=True,
            description='Install a single header only.')

    version('1.1.5', sha256='767dc1718e53678cbea00977adcd0a8a195802a505aec3c537664cf25a173142')
    version('1.1.4', sha256='ed3f9cc32e4ea6075c26caff63ee14a87e43dee1f3010c02bd041b9a0c86f72d')
    version('1.1.3', sha256='a8132befb6b32bf447a74f7e758ac0b63e7bab86974aeb55ee2fd1cd77385f9e')
    version('1.1.2', sha256='87c8e9440cc339c2a7b7efa0313070ff0081eca7780f098f6aff624ffa640c16')
    version('1.1.1', sha256='10915a49a94d371f05af360d40e9cc9615ab86f200d261edf196a8ddd7efa7f8')
    version('1.1.0', sha256='29ca29d843150aabad702356f79009f5b30dda05ac9674a064362b7edcba5477')

    @when('+single_header')
    def cmake(self, spec, prefix):
        pass

    @when('+single_header')
    def build(self, spec, prefix):
        pass

    @when('+single_header')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree('single_include', prefix.include)
