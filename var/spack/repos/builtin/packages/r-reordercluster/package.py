# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReordercluster(RPackage):
    """Reordering the dendrogram according to the class labels.

    Tools for performing the leaf reordering for the dendrogram that preserves
    the hierarchical clustering result and at the same time tries to group
    instances from the same class together."""

    cran = "ReorderCluster"

    version("2.0", sha256="38862ba2ef2a88ea70b12d50352a96f3b2ea032861256702387989bdfb20017f")
    version("1.0", sha256="a87898faa20380aac3e06a52eedcb2f0eb2b35ab74fdc3435d40ee9f1d28476b")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@2.13.0:", type=("build", "run"), when="@2.0:")
    depends_on("r-gtools", type=("build", "run"), when="@2.0:")
    depends_on("r-gplots", type=("build", "run"))
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.1:", type=("build", "run"), when="@2.0:")
