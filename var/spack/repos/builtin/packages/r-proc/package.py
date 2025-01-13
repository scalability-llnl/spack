# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProc(RPackage):
    """Display and Analyze ROC Curves.

    Tools for visualizing, smoothing and comparing receiver operating
    characteristic (ROC curves). (Partial) area under the curve (AUC) can be
    compared with statistical tests based on U-statistics or bootstrap.
    Confidence intervals can be computed for (p)AUC or ROC curves."""

    cran = "pROC"

    version("1.18.5", sha256="5593c841a6df5a2f2d209d0c14401971eb9427092ed9c3ac2059273807b42c89")
    version("1.18.0", sha256="d5ef54b384176ece6d6448014ba40570a98181b58fee742f315604addb5f7ba9")
    version("1.17.0.1", sha256="221c726ffb81b04b999905effccfd3a223cd73cae70d7d86688e2dd30e51a6bd")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-rcpp@0.11.1:", type=("build", "run"))
