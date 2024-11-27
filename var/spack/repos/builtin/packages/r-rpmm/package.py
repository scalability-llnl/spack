# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpmm(RPackage):
    """Recursively Partitioned Mixture Model.

    Recursively Partitioned Mixture Model for Beta and Gaussian Mixtures. This
    is a model-based clustering algorithm that returns a hierarchy of classes,
    similar to hierarchical clustering, but also similar to finite mixture
    models."""

    cran = "RPMM"

    version("1.25", sha256="f04a524b13918062616beda50c4e759ce2719ce14150a0e677d07132086c88c8")

    depends_on("r@2.3.12:", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
