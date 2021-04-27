# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSandwich(RPackage):
    """Robust Covariance Matrix Estimators

    Object-oriented software for model-robust covariance matrix estimators.
    Starting out from the basic  robust Eicker-Huber-White sandwich covariance
    methods include: heteroscedasticity-consistent (HC) covariances for
    cross-section data; heteroscedasticity- and autocorrelation-consistent
    (HAC) covariances for time series data (such as Andrews' kernel HAC,
    Newey-West, and WEAVE estimators); clustered covariances (one-way and
    multi-way); panel and panel-corrected covariances;
    outer-product-of-gradients covariances; and (clustered) bootstrap
    covariances. All methods are applicable to (generalized) linear model
    objects fitted by lm() and glm() but can also be adapted to other classes
    through S3 methods. Details can be found in Zeileis et al. (2020)
    <doi:10.18637/jss.v095.i01>, Zeileis (2004) <doi:10.18637/jss.v011.i10> and
    Zeileis (2006) <doi:10.18637/jss.v016.i09>."""

    homepage = "https://cloud.r-project.org/package=sandwich"
    url      = "https://cloud.r-project.org/src/contrib/sandwich_2.3-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sandwich"

    version('3.0-0', sha256='828fe53b5e09db5015efd529b2db4dcd40251bce110fea7b0b219fa9ac36d529')
    version('2.5-1', sha256='dbef6f4d12b83e166f9a2508b7c732b04493641685d6758d29f3609e564166d6')
    version('2.5-0', sha256='6cc144af20739eb23e5539010d3833d7c7fc53cbca2addb583ab933167c11399')
    version('2.3-4', sha256='2052f7e3d19a05c372f422c5480f1058a4107e420cd038a9bd7240c4f0746d4d')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r@3.0.0:', when='@3.0-0:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
