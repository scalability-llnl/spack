# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRsvd(RPackage):
    """Randomized Singular Value Decomposition.

    Low-rank matrix decompositions are fundamental tools and widely used for
    data analysis, dimension reduction, and data compression. Classically,
    highly accurate deterministic matrix algorithms are used for this task.
    However, the emergence of large-scale data has severely challenged our
    computational ability to analyze big data. The concept of randomness has
    been demonstrated as an effective strategy to quickly produce approximate
    answers to familiar problems such as the singular value decomposition
    (SVD). The rsvd package provides several randomized matrix algorithms such
    as the randomized singular value decomposition (rsvd), randomized principal
    component analysis (rpca), randomized robust principal component analysis
    (rrpca), randomized interpolative decomposition (rid), and the randomized
    CUR decomposition (rcur). In addition several plot functions are provided.
    The methods are discussed in detail by Erichson et al. (2016)
    <arXiv:1608.02148>."""

    cran = "rsvd"

    license("GPL-3.0-or-later")

    version("1.0.5", sha256="e40686b869acd4f71fdb1e8e7a6c64cd6792fc9d52a78f9e559a7176ab84e21e")
    version("1.0.3", sha256="13560e0fc3ae6927c4cc4d5ad816b1f640a2a445b712a5a612ab17ea0ce179bb")
    version("1.0.2", sha256="c8fe5c18bf7bcfe32604a897e3a7caae39b49e47e93edad9e4d07657fc392a3a")

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.0.5:")
    depends_on("r-matrix", type=("build", "run"))
