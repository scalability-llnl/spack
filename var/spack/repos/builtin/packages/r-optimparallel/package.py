# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROptimparallel(RPackage):
    """Parallel Version of the L-BFGS-B Optimization Method.

    Provides a parallel version of the L-BFGS-B method of optim(). The main
    function of the package is optimParallel(), which has the same usage and
    output as optim(). Using optimParallel() can significantly reduce the
    optimization time."""

    cran = "optimParallel"

    version("1.0-2", sha256="0f9bc62c23d9005130f2892bf5eaecf308fa48a727bdd5e19b7dcd1d95f30a9d")

    depends_on("r@3.5:", type=("build", "run"))
