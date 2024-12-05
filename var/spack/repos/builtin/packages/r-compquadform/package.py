# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCompquadform(RPackage):
    """Distribution Function of Quadratic Forms in Normal Variables.

    Computes the distribution function of quadratic forms in normal variables
    using Imhof's method, Davies's algorithm, Farebrother's algorithm or Liu et
    al.'s algorithm."""

    cran = "CompQuadForm"

    version("1.4.3", sha256="042fc56c800dd8f5f47a017e2efa832caf74f0602824abf7099898d9708660c4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
