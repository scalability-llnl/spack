# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYaimpute(RPackage):
    """Nearest Neighbor Observation Imputation and Evaluation Tools.

    Performs nearest neighbor-based imputation using one or more alternative
    approaches to processing multivariate data. These include methods based on
    canonical correlation analysis, canonical correspondence analysis, and a
    multivariate adaptation of the random forest classification and regression
    techniques of Leo Breiman and Adele Cutler. Additional methods are also
    offered. The package includes functions for comparing the results from
    running alternative techniques, detecting imputation targets that are
    notably distant from reference observations, detecting and correcting for
    bias, bootstrapping and building ensemble imputations, and mapping
    results."""

    cran = "yaImpute"

    version("1.0-34", sha256="b4c898c95fca784480bbbc239c78c85dc9f45a96c34c563ea7e81248ef8a8a73")
    version("1.0-33", sha256="58595262eb1bc9ffeeadca78664c418ea24b4e894744890c00252c5ebd02512c")
    version("1.0-32", sha256="08eee5d851b80aad9c7c80f9531aadd50d60e4b16b3a80657a50212269cd73ff")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"), when="@1.0-33:")
