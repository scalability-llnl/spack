# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPvclust(RPackage):
    """Hierarchical Clustering with P-Values via Multiscale Bootstrap
    Resampling.

    An implementation of multiscale bootstrap resampling for assessing the
    uncertainty in hierarchical cluster analysis. It provides SI (selective
    inference) p-value, AU (approximately unbiased) p-value and BP (bootstrap
    probability) value for each cluster in a dendrogram."""

    cran = "pvclust"

    license("GPL-2.0-or-later")

    version("2.2-0", sha256="7892853bacd413b5a921006429641ad308a344ca171b3081c15e4c522a8b0201")

    depends_on("r@2.10.0:", type=("build", "run"))
