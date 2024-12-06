# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Volk(CMakePackage):
    """VOLK is the Vector-Optimized Library of Kernels. It is a
    library that contains kernels of hand-written SIMD code for
    different mathematical operations. Since each SIMD architecture
    can be very different and no compiler has yet come along to handle
    vectorization properly or highly efficiently, VOLK approaches the
    problem differently.

    For each architecture or platform that a developer wishes to
    vectorize for, a new proto-kernel is added to VOLK. At runtime,
    VOLK will select the correct proto-kernel. In this way, the users
    of VOLK call a kernel for performing the operation that is
    platform/architecture agnostic. This allows us to write portable
    SIMD code."""

    homepage = "https://github.com/gnuradio/volk"
    url = "https://github.com/gnuradio/volk/archive/v2.3.0.tar.gz"

    maintainers("aweits")

    license("GPL-3.0-or-later")

    version("2.3.0", sha256="f42c928f561b128acfe4adb21227e4a62a3f6ab8103592fc3233765ff326d5fc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-mako@0.4.2:", type=("build", "run"))
