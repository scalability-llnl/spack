# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Assimp(CMakePackage):
    """Open Asset Import Library (Assimp) is a portable Open Source library to
    import various well-known 3D model formats in a uniform manner."""

    homepage = "https://www.assimp.org"
    url      = "https://github.com/assimp/assimp/archive/v4.0.1.tar.gz"
    git      = "https://github.com/assimp/assimp.git"

    version('master', branch='master')
    version('5.0.1', sha256='11310ec1f2ad2cd46b95ba88faca8f7aaa1efe9aa12605c55e3de2b977b3dbfc')
    version('4.0.1', sha256='60080d8ab4daaab309f65b3cffd99f19eb1af8d05623fff469b9b652818e286e')

    variant('shared',  default=True,
            description='Enables the build of shared libraries')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    def cmake_args(self):
        args = [
            '-DASSIMP_BUILD_TESTS=OFF',
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in self.spec else 'OFF'),
        ]
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
