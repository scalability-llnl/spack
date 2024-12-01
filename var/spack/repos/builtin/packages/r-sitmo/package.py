# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSitmo(RPackage):
    """Parallel Pseudo Random Number Generator (PPRNG) 'sitmo' Header Files.

    Provided within are two high quality and fast PPRNGs that may be used in an
    'OpenMP' parallel environment. In addition, there is a generator for one
    dimensional low-discrepancy sequence. The objective of this library to
    consolidate the distribution of the 'sitmo' (C++98 & C++11), 'threefry' and
    'vandercorput' (C++11-only) engines on CRAN by enabling others to link to
    the header files inside of 'sitmo' instead of including a copy of each
    engine within their individual package. Lastly, the package contains
    example implementations using the 'sitmo' package and three accompanying
    vignette that provide additional information."""

    cran = "sitmo"

    license("MIT")

    version("2.0.2", sha256="448ef8d56e36783354011845daf33f1efb83ea3b9685eea75eaf5134e24fa8c2")
    version("2.0.1", sha256="0c90d357af334d5c99c8956739dc12623ddd87dda5efa59f4a43f7393c87ed2a")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.13:", type=("build", "run"))
