# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClustergeneration(RPackage):
    """Random Cluster Generation (with Specified Degree of Separation).

    We developed the clusterGeneration package to provide functions  for
    generating random clusters, generating random  covariance/correlation
    matrices, calculating a separation index (data and population version) for
    pairs of clusters or cluster distributions, and 1-D and 2-D projection
    plots to visualize clusters.  The package also contains a function to
    generate random clusters based on factorial designs with factors such as
    degree of separation, number of clusters, number of variables, number of
    noisy variables."""

    cran = "clusterGeneration"

    version("1.3.8", sha256="0f842256582ab41bcd00ee08ea6d7e231ff362fe0156a53347873e9636f73a70")
    version("1.3.7", sha256="534f29d8f7ed11e6e9a496f15845b588ec7133f3da5e6def8140b88500e52d5c")
    version("1.3.4", sha256="7c591ad95a8a9d7fb0e4d5d80dfd78f7d6a63cf7d11eb53dd3c98fdfb5b868aa")

    depends_on("r@2.9.1:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.3.7:")
    depends_on("r-mass", type=("build", "run"))
