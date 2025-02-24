# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpackCompilerWrapper(MakefilePackage):
    """An LD_PRELOAD'able exec() family symbol intercepting compiler wrapper
    for Spack on Linux."""

    homepage = "https://github.com/haampie/spack-compiler-wrapper"
    url      = "https://github.com/haampie/spack-compiler-wrapper/archive/refs/tags/v0.1.1.tar.gz"

    maintainers = ['haampie']

    version('0.1.1', sha256='66a0bf60a710236173823988294ef68419a73e63cea4a455a248b8faa506201b')

    def install(self, spec, prefix):
        make('install', 'prefix={}'.format(prefix))
