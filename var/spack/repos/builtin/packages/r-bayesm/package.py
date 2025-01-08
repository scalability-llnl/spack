# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBayesm(RPackage):
    """Bayesian Inference for Marketing/Micro-Econometrics.

    Covers many important models used in marketing and micro-econometrics
    applications.  The package includes: Bayes Regression (univariate or
    multivariate dep var), Bayes Seemingly Unrelated Regression (SUR), Binary
    and Ordinal Probit, Multinomial Logit (MNL) and Multinomial Probit (MNP),
    Multivariate Probit, Negative Binomial (Poisson) Regression, Multivariate
    Mixtures of Normals (including clustering), Dirichlet Process Prior Density
    Estimation with normal base, Hierarchical Linear Models with normal prior
    and covariates, Hierarchical Linear Models with a mixture of normals prior
    and covariates, Hierarchical Multinomial Logits with a mixture of normals
    prior and covariates, Hierarchical Multinomial Logits with a Dirichlet
    Process prior and covariates, Hierarchical Negative Binomial Regression
    Models, Bayesian analysis of choice-based conjoint data, Bayesian treatment
    of linear instrumental variables models, Analysis of Multivariate Ordinal
    survey data with scale usage heterogeneity (as in Rossi et al, JASA (01)),
    Bayesian Analysis of Aggregate Random Coefficient Logit Models as in BLP
    (see Jiang, Manchanda, Rossi 2009) For further reference, consult our book,
    Bayesian Statistics and Marketing by Rossi, Allenby and McCulloch (Wiley
    2005) and Bayesian Non- and Semi-Parametric Methods and Applications
    (Princeton U Press 2014)."""

    cran = "bayesm"

    license("GPL-2.0-or-later")

    version("3.1-6", sha256="17d72b9cdc090845f98e7a04640380d0baef8bc23d1487c8f64dc192fdb93cb5")
    version("3.1-5", sha256="f223074ca41ede293b48350eac77a565e034f0f8cf3dd72d0e1d126cc58047a2")
    version("3.1-4", sha256="061b216c62bc72eab8d646ad4075f2f78823f9913344a781fa53ea7cf4a48f94")
    version("3.1-3", sha256="51e4827eca8cd4cf3626f3c2282543df7c392b3ffb843f4bfb386fe104642a10")
    version("3.1-2", sha256="a332f16e998ab10b17a2b1b9838d61660c36e914fe4d2e388a59f031d52ad736")
    version("3.1-1", sha256="4854517dec30ab7c994de862aae1998c2d0c5e71265fd9eb7ed36891d4676078")
    version("3.1-0.1", sha256="5879823b7fb6e6df0c0fe98faabc1044a4149bb65989062df4ade64e19d26411")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.0:", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
