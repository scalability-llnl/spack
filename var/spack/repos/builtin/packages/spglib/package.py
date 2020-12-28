# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spglib(CMakePackage):
    """C library for finding and handling crystal symmetries."""

    homepage = "https://atztogo.github.io/spglib/"
    url      = "https://github.com/atztogo/spglib/archive/v1.10.3.tar.gz"

    patch('fix_cmake_install.patch', when='@:1.10.3')
    # patch by Krishnendu Ghosh
    patch('fix_cpp.patch', when='@:1.10.3')

    version('1.10.3', sha256='43776b5fb220b746d53c1aa39d0230f304687ec05984671392bccaf850d9d696')
    version('1.10.0', sha256='117fff308731784bea2ddaf3d076f0ecbf3981b31ea1c1bfd5ce4f057a5325b1')

    @property
    def libs(self):
        return find_libraries(['libsymspg'], root=self.prefix.lib,
                              recursive=False)
