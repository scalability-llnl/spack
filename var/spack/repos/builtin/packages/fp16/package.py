# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fp16(Package):
    """FP16 is a header-only library for
    conversion to/from half-precision floating point formats"""

    homepage = "https://github.com/Maratyszcza/FP16/"
    git      = "https://github.com/Maratyszcza/FP16.git"

    version('master')

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
