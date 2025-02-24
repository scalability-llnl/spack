# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPan(RPackage):
    """Multiple imputation for multivariate panel or clustered data.

    It provides functions and examples for maximum likelihood estimation for
    generalized linear mixed models and Gibbs sampler for multivariate linear
    mixed models with incomplete data, as described in Schafer JL (1997)
    "Imputation of missing covariates under a multivariate linear mixed model".
    Technical report 97-04, Dept. of Statistics, The Pennsylvania State
    University."""

    cran = "pan"

    license("GPL-3.0-only")

    version("1.9", sha256="cd91232d653783ea7f34c0eebaa80c472b5501b21eea500c4c1a8e57116c6eea")
    version("1.6", sha256="adc0df816ae38bc188bce0aef3aeb71d19c0fc26e063107eeee71a81a49463b6")
    version("1.4", sha256="e6a83f0799cc9714f5052f159be6e82ececd013d1626f40c828cda0ceb8b76dc")

    depends_on("r@2.10:", when="@1.9:", type=("build", "run"))
