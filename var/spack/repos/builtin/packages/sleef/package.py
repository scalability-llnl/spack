# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sleef(CMakePackage):
    """SIMD Library for Evaluating Elementary Functions,
    vectorized libm and DFT."""

    homepage = "http://sleef.org"
    url      = "https://github.com/shibatch/sleef/archive/3.2.tar.gz"

    version('3.2', sha256='3130c5966e204e6d6a3ace81e543d12b5b21f60897f1c185bfa587c1bd77bee2')
