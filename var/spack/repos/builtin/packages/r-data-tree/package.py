# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDataTree(RPackage):
    """Create tree structures from hierarchical data, and traverse the
    tree in various orders. Aggregate, cumulate, print, plot, convert to
    and from data.frame and more. Useful for decision trees, machine
    learning, finance, conversion from and to JSON, and many other
    applications."""

    cran = "data.tree"

    maintainers = "viniciusvgp"

    version("1.0.0", sha256="40674c90a5bd00f5185db9adbd221c6f1114043e69095249f5fa8b3044af3f5e")

    depends_on("r-stringi", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
