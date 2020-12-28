# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Collier(CMakePackage):
    """COLLIER: A Complex One-Loop LIbrary with Extended Regularizations """

    homepage = "https://collier.hepforge.org"
    url      = "https://collier.hepforge.org/downloads/?f=collier-1.2.5.tar.gz"

    tags = ['hep']

    version('1.2.5', sha256='3ec58a975ff0c3b1ca870bc38973476c923ff78fd3dd5850e296037852b94a8b')
    version('1.2.4', sha256='92ae8f61461b232fbd47a6d8e832e1a726d504f9390b7edc49a68fceedff8857')
    version('1.2.3', sha256='e6f72df223654df59113b0067a4bebe9f8c20227bb81371d3193e1557bdf56fb')
    version('1.2.2', sha256='140029e36635565262719124dcda2fa7d66fd468442cb268f6da16d4cbbab29a')
    version('1.2.1', sha256='7f5bc81a00de071e2451ba3e11cad726df0ae18bd973dba4aeba165897d48c2d')
    version('1.2.0', sha256='e5b2def953d7f9f4f2cacd4616aa65c77e2b9adf7eed2ca3531b993e529fbafd')
    version('1.1',   sha256='80fd54e2c30029d3d7d646738ae9469ad3a6f5ea7aa1179b951030df048e36bc')
    version('1.0',   sha256='54f40c1ed07a6829230af400abfe48791e74e56eac2709c0947cec3410a4473d')

    @property
    def parallel(self):
        return not self.spec.satisfies('@:1.2.4')

    def cmake_args(self):
        args = ['-Dstatic=ON']
        return args
