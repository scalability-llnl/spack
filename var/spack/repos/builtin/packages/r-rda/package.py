# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRda(RPackage):
    """Shrunken Centroids Regularized Discriminant Analysis.

    Shrunken Centroids Regularized Discriminant Analysis for the classification
    purpose in high dimensional data."""

    cran = "rda"

    license("GPL-3.0-or-later")

    version("1.2-1", sha256="37038a9131c9133519f5e64fa1a86dbe28b21f519cf6528503234648a139ae9a")
    version("1.0.2-2.1", sha256="eea3a51a2e132a023146bfbc0c384f5373eb3ea2b61743d7658be86a5b04949e")
    version("1.0.2-2", sha256="52ee41249b860af81dc692eee38cd4f8f26d3fbe34cb274f4e118de0013b58bc")
    version("1.0.2-1", sha256="e5b96610ec9e82f12efe5dbb9a3ec9ecba9aaddfad1d6ab3f8c37d15fc2b42b7")

    depends_on("r@2.10:", type=("build", "run"))
