# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRann(RPackage):
    """Fast Nearest Neighbour Search (Wraps ANN Library) Using L2 Metric.

    Finds the k nearest neighbours for every point in a given dataset in O(N
    log N) time using Arya and Mount's ANN library (v1.1.3). There is support
    for approximate as well as exact searches, fixed radius searches and 'bd'
    as well as 'kd' trees. The distance is computed using the L2 (Euclidean)
    metric. Please see package 'RANN.L1' for the same functionality using the
    L1 (Manhattan, taxicab) metric."""

    cran = "RANN"

    version("2.6.1", sha256="b299c3dfb7be17aa41e66eff5674fddd2992fb6dd3b10bc59ffbf0c401697182")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
