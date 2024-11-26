# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    url = "https://github.com/simd-everywhere/simde/archive/v0.6.0.tar.gz"
    git = "https://github.com/simd-everywhere/simde.git"

    license("MIT")

    version("0.7.6", sha256="c63e6c61392e324728da1c7e5de308cb31410908993a769594f5e21ff8de962b")
    version("0.7.2", sha256="366d5e9a342c30f1e40d1234656fb49af5ee35590aaf53b3c79b2afb906ed4c8")
    version("0.6.0", sha256="25a8b8c69c17ddc2f6209e86caa6b12d4ed91c0f841617efc56e5675eea84915")

    depends_on("c", type="build")  # generated

    patch("sve-gcc.patch", when="@0.6.0 %gcc")
    conflicts("%gcc@8", when="target=a64fx", msg="Internal compiler error with gcc8 and a64fx")
