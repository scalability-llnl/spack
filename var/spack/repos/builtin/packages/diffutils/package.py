# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Diffutils(AutotoolsPackage, GNUMirrorPackage):
    """GNU Diffutils is a package of several programs related to finding
    differences between files."""

    homepage = "https://www.gnu.org/software/diffutils/"
    gnu_mirror_path = "diffutils/diffutils-3.7.tar.xz"

    version('3.7', sha256='b3a7a6221c3dc916085f0d205abf6b8e1ba443d4dd965118da364a1dc1cb3a26')
    version('3.6', sha256='d621e8bdd4b573918c8145f7ae61817d1be9deb4c8d2328a65cea8e11d783bd6')

    build_directory = 'spack-build'

    depends_on('libiconv')

    def setup_build_environment(self, spack_env):
        if self.spec.satisfies('%clang@9:'):
            spack_env.append_flags('CFLAGS',
                                   '-Werror=implicit-function-declaration')
