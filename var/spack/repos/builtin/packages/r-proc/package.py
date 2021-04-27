# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RProc(RPackage):
    """Display and Analyze ROC Curves

    Tools for visualizing, smoothing and comparing receiver operating
    characteristic (ROC curves). (Partial) area under the curve (AUC) can be
    compared with statistical tests based on U-statistics or bootstrap.
    Confidence intervals can be computed for (p)AUC or ROC curves."""

    homepage = "http://expasy.org/tools/pROC/"
    url      = "https://cloud.r-project.org/src/contrib/pROC_1.17.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pROC"

    version('1.17.0.1', sha256='221c726ffb81b04b999905effccfd3a223cd73cae70d7d86688e2dd30e51a6bd')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-rcpp@0.11.1:', type=('build', 'run'))
