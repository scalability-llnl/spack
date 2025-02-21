# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMetadat(RPackage):
    """Meta-Analysis Datasets.

    A collection of meta-analysis datasets for teaching purposes,
    illustrating/testing meta-analytic methods, and validating published
    analyses."""

    cran = "metadat"

    license("GPL-2.0-or-later")

    version("1.2-0", sha256="f0cce5e30c3d256eaf5a41e4f52ffc7108e195016a4b99409e0ab4c2ef58f5b8")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r-mathjaxr", type=("build", "run"))
