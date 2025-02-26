# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSparsearray(RPackage):
    """High-performance sparse data representation and manipulation in R."""

    bioc = "SparseArray"

    version("1.6.0", commit="c665d9eb675881e651e24afa6f098eb5fd13dcb0")
    version("1.4.8", commit="3d08cdc5d7723b74cef6b10fd7fa70cb242f31cd")
    version("1.2.4", commit="5ece9d3ea94373d08f703197c3308e364c56872b")

    depends_on("r@4.3.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.43.1:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrixgenerics@1.11.1:", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-s4arrays@1.5.11:", type=("build", "run"))
    depends_on("r-s4vectors@0.43.2:", type=("build", "run"))
    depends_on("r-xvector", type=("build", "run"))
