# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brotli(CMakePackage):
    """Brotli is a generic-purpose lossless compression algorithm"""

    homepage = "https://github.com/google/brotli"
    url      = "https://github.com/google/brotli/archive/v1.0.7.tar.gz"

    version('1.0.7', sha256='4c61bfb0faca87219ea587326c467b95acb25555b53d1a421ffa3c8a9296ee2c')

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies('platform=darwin'):
            fix_darwin_install_name(self.prefix.lib)
