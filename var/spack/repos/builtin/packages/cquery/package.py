# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cquery(CMakePackage):
    """a C++ header-only library for Nearest Neighbor (NN) search wih KD-trees.
    """

    homepage = "https://github.com/cquery-project/cquery"
    git      = "https://github.com/cquery-project/cquery.git"

    version('2018-08-23', commit='70c755b2e390d3edfb594a84a7531beb26b2bc07',
            submodules=True)

    depends_on('llvm')

    def cmake_args(self):
        args = ['-DCMAKE_EXPORT_COMPILE_COMMANDS=YES',
                '-DSYSTEM_CLANG=ON']
        return args
