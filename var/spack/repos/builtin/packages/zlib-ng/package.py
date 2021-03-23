# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ZlibNg(CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url      = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"

    version('2.0.0', sha256='86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8')

    variant('compat', default=False, description='Enable compatibility API')
    variant('opt', default=True, description='Enable optimizations')

    depends_on('cmake@3.5.1:', type='build')

    def cmake_args(self):
        args = [
            self.define_from_variant('ZLIB_COMPAT', 'compat'),
            self.define_from_variant('WITH_OPTIM', 'opt'),
        ]

        return args
