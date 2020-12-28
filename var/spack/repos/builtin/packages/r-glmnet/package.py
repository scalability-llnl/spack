# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlmnet(RPackage):
    """Extremely efficient procedures for fitting the entire lasso or
    elastic-net regularization path for linear regression, logistic and
    multinomial regression models, Poisson regression and the Cox model. Two
    recent additions are the multiple-response Gaussian, and the grouped
    multinomial. The algorithm uses cyclical coordinate descent in a path-wise
    fashion, as described in the paper linked to via the URL below."""

    homepage = "https://cloud.r-project.org/package=glmnet"
    url      = "https://cloud.r-project.org/src/contrib/glmnet_2.0-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/glmnet"

    version('2.0-18', sha256='e8dce9d7b8105f9cc18ba981d420de64a53b09abee219660d3612915d554256b')
    version('2.0-13', sha256='f3288dcaddb2f7014d42b755bede6563f73c17bc87f8292c2ef7776cb9b9b8fd')
    version('2.0-5', sha256='2ca95352c8fbd93aa7800f3d972ee6c1a5fcfeabc6be8c10deee0cb457fd77b1')

    depends_on('r-matrix@1.0-6:', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
