# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKernlab(RPackage):
    """Kernel-based machine learning methods for classification, regression,
    clustering, novelty detection, quantile regression and dimensionality
    reduction. Among other methods 'kernlab' includes Support Vector Machines,
    Spectral Clustering, Kernel PCA, Gaussian Processes and a QP solver."""

    homepage = "https://cloud.r-project.org/package=kernlab"
    url      = "https://cloud.r-project.org/src/contrib/kernlab_0.9-25.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/kernlab"

    version('0.9-27', sha256='f6add50ed4097f04d09411491625f8d46eafc4f003b1c1cff78a6fff8cc31dd4')
    version('0.9-26', sha256='954940478c6fcf60433e50e43cf10d70bcb0a809848ca8b9d683bf371cd56077')
    version('0.9-25', sha256='b9de072754bb03c02c4d6a5ca20f2290fd090de328b55ab334ac0b397ac2ca62')

    depends_on('r@2.10:', type=('build', 'run'))
