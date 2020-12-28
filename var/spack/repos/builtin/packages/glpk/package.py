# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glpk(AutotoolsPackage, GNUMirrorPackage):
    """The GLPK (GNU Linear Programming Kit) package is intended for solving
    large-scale linear programming (LP), mixed integer programming
    (MIP), and other related problems. It is a set of routines written
    in ANSI C and organized in the form of a callable library.
    """

    homepage = "https://www.gnu.org/software/glpk"
    gnu_mirror_path = "glpk/glpk-4.65.tar.gz"

    version('4.65', sha256='4281e29b628864dfe48d393a7bedd781e5b475387c20d8b0158f329994721a10')
    version('4.61', sha256='9866de41777782d4ce21da11b88573b66bb7858574f89c28be6967ac22dfaba9')
    version('4.57', sha256='7323b2a7cc1f13e45fc845f0fdca74f4daea2af716f5ad2d4d55b41e8394275c')

    variant(
        'gmp', default=False, description='Activates support for GMP library'
    )

    depends_on('gmp', when='+gmp')

    def configure_args(self):

        options = []

        if '+gmp' in self.spec:
            options.append('--with-gmp')

        return options
