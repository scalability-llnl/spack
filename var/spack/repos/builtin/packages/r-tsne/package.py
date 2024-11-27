# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTsne(RPackage):
    """T-Distributed Stochastic Neighbor Embedding for R (t-SNE).

    A "pure R" implementation of the t-SNE algorithm."""

    cran = "tsne"

    license("GPL-2.0-or-later")

    version("0.1-3.1", sha256="14abc65bc0a3f3ed63c04dda19620e483a21d1f5f33feb74aba9f3221434d888")
    version("0.1-3", sha256="66fdf5d73e69594af529a9c4f261d972872b9b7bffd19f85c1adcd66afd80c69")
    version("0.1-2", sha256="c6c3455e0f0f5dcac14299b3dfeb1a5f1bfe5623cdaf602afc892491d3d1058b")
    version("0.1-1", sha256="c953991215a660cf144e55848d2507bcf7932618e164b0e56901fb33831fd1d3")
