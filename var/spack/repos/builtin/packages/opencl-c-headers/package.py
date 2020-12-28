# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class OpenclCHeaders(Package):
    """OpenCL (Open Computing Language) C header files"""

    homepage = "https://www.khronos.org/registry/OpenCL/"
    url      = "https://github.com/KhronosGroup/OpenCL-Headers/archive/v2020.06.16.tar.gz"

    version('2020.06.16', sha256='2f5a60e5ac4b127650618c58a7e3b35a84dbf23c1a0ac72eb5e7baf221600e06')
    version('2020.03.13', sha256='664bbe587e5a0a00aac267f645b7c413586e7bc56dca9ff3b00037050d06f476')

    def install(self, spec, prefix):
        install_tree('CL', prefix.include.CL)
        if sys.platform == 'darwin':
            ln = which('ln')
            ln('-s', prefix.include.CL, prefix.include.OpenCL)
