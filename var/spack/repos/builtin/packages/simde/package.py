# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Simde(MesonPackage):
    """The SIMDe header-only library provides fast, portable
       implementations of SIMD intrinsics on hardware which doesn't
       natively support them, such as calling SSE functions on ARM.
       There is no performance penalty if the hardware supports the
       native implementation (e.g., SSE/AVX runs at full speed on x86,
       NEON on ARM, etc.)."""

    homepage = "https://github.com/simd-everywhere/simde"
    url      = "https://github.com/simd-everywhere/simde/archive/v0.6.0.tar.gz"
    git      = "https://github.com/simd-everywhere/simde.git"

    version('0.6.0', sha256='25a8b8c69c17ddc2f6209e86caa6b12d4ed91c0f841617efc56e5675eea84915')

    patch('sve-gcc.patch', when='@0.6.0 %gcc')
    conflicts('%gcc@8', when='target=a64fx',
              msg='Internal compiler error with gcc8 and a64fx')
