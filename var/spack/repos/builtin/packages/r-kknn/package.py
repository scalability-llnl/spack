# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKknn(RPackage):
    """Weighted k-Nearest Neighbors.

    Weighted k-Nearest Neighbors for Classification, Regression and
    Clustering."""

    cran = "kknn"

    license("GPL-2.0-or-later")

    version("1.3.1", sha256="22840e70ec2afa40371e274b583634c8f6d27149a87253ee411747d5db78f3db")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-igraph@1.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
